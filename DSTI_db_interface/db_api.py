# Standard library imports
import configparser
import hashlib
import os

# Local Imports
from .db_connection import provide_db_connection

# External library imports
import pandas as pd
import pyodbc


class NonPermittedQuery(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        # print('calling str')
        if self.message:
            return "NonPermittedQuery, {0} ".format(self.message)
        else:
            return "NonPermittedQuery has been raised"


CHECKPOINT_PATH = os.path.join(
    os.path.join(os.path.dirname(__file__)), "data", "survey_data_last_checkpoint.txt"
)

AllSurveyData_QRY = """

                            SELECT
                                    UserId
                                    , 1 as SurveyId
                                    , 
                            COALESCE(
                                (
                                    SELECT a.Answer_Value
                                    FROM Answer as a
                                    WHERE
                                        a.UserId = u.UserId
                                        AND a.SurveyId = 1
                                        AND a.QuestionId = 1
                                ), -1) AS ANS_Q1  , 
                            COALESCE(
                                (
                                    SELECT a.Answer_Value
                                    FROM Answer as a
                                    WHERE
                                        a.UserId = u.UserId
                                        AND a.SurveyId = 1
                                        AND a.QuestionId = 2
                                ), -1) AS ANS_Q2  ,  NULL AS ANS_Q3  ,  NULL AS ANS_Q4 
                            FROM
                                [User] as u
                            WHERE EXISTS
                            (
                                    SELECT *
                                    FROM Answer as a
                                    WHERE u.UserId = a.UserId
                                    AND a.SurveyId = 1
                            )
                            UNION 
                            SELECT
                                    UserId
                                    , 2 as SurveyId
                                    ,  NULL AS ANS_Q1  , 
                            COALESCE(
                                (
                                    SELECT a.Answer_Value
                                    FROM Answer as a
                                    WHERE
                                        a.UserId = u.UserId
                                        AND a.SurveyId = 2
                                        AND a.QuestionId = 2
                                ), -1) AS ANS_Q2  , 
                            COALESCE(
                                (
                                    SELECT a.Answer_Value
                                    FROM Answer as a
                                    WHERE
                                        a.UserId = u.UserId
                                        AND a.SurveyId = 2
                                        AND a.QuestionId = 3
                                ), -1) AS ANS_Q3  ,  NULL AS ANS_Q4 
                            FROM
                                [User] as u
                            WHERE EXISTS
                            (
                                    SELECT *
                                    FROM Answer as a
                                    WHERE u.UserId = a.UserId
                                    AND a.SurveyId = 2
                            )
                            UNION 
                            SELECT
                                    UserId
                                    , 3 as SurveyId
                                    ,  NULL AS ANS_Q1  ,  NULL AS ANS_Q2  ,  NULL AS ANS_Q3  ,  NULL AS ANS_Q4 
                            FROM
                                [User] as u
                            WHERE EXISTS
                            (
                                    SELECT *
                                    FROM Answer as a
                                    WHERE u.UserId = a.UserId
                                    AND a.SurveyId = 3
                            )
                                
"""

create_vw_AllSurveyData_qry = f"""
                CREATE VIEW [dbo].[vw_AllSurveyData] AS 
                    {AllSurveyData_QRY}
"""


def is_permitted_query(sql_query):
    qry = sql_query.lower()
    select_only_qry = not any(
        [name in qry for name in ("update", "drop", "delete", "create", "alter")]
    )
    non_empty_qry = qry is not None and qry != ""
    permitted_qry = select_only_qry and non_empty_qry
    return permitted_qry


@provide_db_connection
def run_sql_select_query(sql_query=None, connection=None):
    """
    Runs passed query against database using CONN object
    """
    if sql_query and connection:
        if not is_permitted_query(sql_query):
            raise NonPermittedQuery
        else:
            df = pd.read_sql(sql_query, connection)
            return df


def get_checkpoint_hash():
    """
    Reads the hash string in the CHECKPOINT_PATH
    and returns it to the caller.

    If the CHECKPOINT_PATH doesn't exist, a blank file is 
    created and None is returned.
    """

    checkpoint_hash = None
    # If CHECKPOINT_PATH doesn't exist, it's probably
    # the first time the code has run
    if not os.path.exists(CHECKPOINT_PATH):
        with open(CHECKPOINT_PATH, "w") as file:
            # Only create file, don't write anything
            pass
    else:
        with open(CHECKPOINT_PATH, "r") as file:
            checkpoint_hash = file.read()

    return checkpoint_hash


def update_vw_AllSurveyData_if_obsolete(live_survey_data: pd.DataFrame) -> bool:
    """
    Returns True is the data in the view vw_AllSurveyData
    is different to that taken from the live tables
    """
    checkpoint_hash = get_checkpoint_hash()
    live_survey_data_hash = get_dataframe_hash_id(live_survey_data)

    # vw_AllSurveyData must be updated if obsolete
    obsolete = checkpoint_hash and (live_survey_data_hash != checkpoint_hash)

    if obsolete or not checkpoint_hash:
        drop_vw_AllSurveyData()
        create_vw_AllSurveyData()
        # Record new checkpoint_hash
        persist_checkpoint_hash(live_survey_data_hash)

    if obsolete:
        print(
            f"vw_AllSurveyData data obsolete. Updating checkpoint: {checkpoint_hash} -> {live_survey_data_hash}"
        )
    elif not checkpoint_hash:
        print(
            f"First checkpoint recorded using current vw_AllSurveyData data: {live_survey_data}"
        )
    elif not obsolete:
        print(
            f"No update to vw_AllSurveyData necessary. Existing checkpoint remains: {checkpoint_hash}"
        )


def persist_checkpoint_hash(live_survey_data_hash):
    # Record new checkpoint_hash
    with open(CHECKPOINT_PATH, "w") as file:
        file.write(live_survey_data_hash)


def get_all_survey_data() -> pd.DataFrame:
    """

    """
    live_survey_data = run_sql_select_query(f"{AllSurveyData_QRY} ORDER BY UserId")

    update_vw_AllSurveyData_if_obsolete(live_survey_data)

    return live_survey_data


def get_dataframe_hash_id(df: pd.DataFrame) -> str:
    """
    Takes a Pandas DataFrame and returns an 
    md5 hash string of its string representation.

    On failure, returns an 'UNKNOWN_HASH' string.
    """
    try:
        hashable_df = df.to_string().encode("UTF-8")
        m = hashlib.md5(hashable_df).hexdigest()
        return m
    except Exception as e:
        return "UNKNOWN_HASH"


@provide_db_connection
def drop_vw_AllSurveyData(connection=None):
    """
    @provide_db_connection provides db connection object
    and closes it after the function completes
    """
    qry = "DROP VIEW [dbo].[vw_AllSurveyData]"
    cur = connection.execute(qry)
    cur.commit()
    cur.close()


@provide_db_connection
def create_vw_AllSurveyData(connection=None):
    """
    @provide_db_connection provides db connection object
    and closes it after the function completes
    """
    cur = connection.execute(create_vw_AllSurveyData_qry)
    cur.commit()
    cur.close()


@provide_db_connection
def trg_refreshSurveyView(connection=None):
    """
    Updates [dbo].[vw_AllSurveyData] view with latest data (always fresh)

    @provide_db_connection provides db connection object
    and closes it after the function completes
    """
    pass


def persist_survey_structure(df: pd.DataFrame, results_name: str) -> None:
    """
    Saves a Pandas dataframe locally as a csv with a
    filename composed of [df_checksum_string]_[results_name].csv.
    """
    pass


def generate_checksum_from_dataframe(df: pd.DataFrame) -> str:
    """
    Generate a checksum representing the contents of a
    Pandas dataframe. Returns a string representation of the checksum.
    """
    pass


def freshen_csv():
    """
    The local csv, may or may not be up to date. We don't know!
    So this here proceedure gonna select all yo mutha fuckin 
    shit from SurveyStructure table y'all. An if dat shit gotta 
    different stank t yo old SurveyStructure,
    we gonna update yo csv and yo [dbo].[vw_AllSurveyData] view.
    """
    pass
