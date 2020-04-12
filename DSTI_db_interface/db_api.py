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


#CONN = get_db_connection()


CHECKPOINT_PATH = os.path.join(
    os.path.join(os.path.dirname(__file__)), "data", "survey_data_last_checkpoint.csv"
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
                CREATE   VIEW [dbo].[vw_AllSurveyData] AS 
                    {AllSurveyData_QRY}
"""




def is_permitted_query(sql_query):
    qry = sql_query.lower()
    select_only_qry = not any(
        [name in qry for name in ('update', 'drop', 'delete', 'create', 'alter')]
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


def checkpoint_file_exists():
    """

    """

    if not os.path.exists(CHECKPOINT_PATH):
        print(
            f"No checkpoint file exists at {CHECKPOINT_PATH}.\nAssuming first execution..."
        )
        return False
    else:
        return True


def run_maintenence_on_vw_AllSurveyData(live_survey_data):
    """

    """

    checkpoint_exists = checkpoint_file_exists()
    live_survey_data_hash = get_dataframe_hash_id(live_survey_data)

    if checkpoint_exists:
        # Does the checkpoint hash match the current data hash
        survey_data_last_checkpoint = pd.read_csv(CHECKPOINT_PATH)
        survey_data_last_checkpoint_hash = get_dataframe_hash_id(
            survey_data_last_checkpoint
        )

        update_required = live_survey_data_hash != survey_data_last_checkpoint_hash

    if not checkpoint_exists:
        # We update the view just in case and better make a checkpoint file
        drop_vw_AllSurveyData()
        create_vw_AllSurveyData()
        live_survey_data.to_csv(CHECKPOINT_PATH)
        print("First checkpoint created: {live_survey_data_hash}")

    if checkpoint_exists and update_required:
        # We better update the view and replace the checkpoint
        drop_vw_AllSurveyData()
        create_vw_AllSurveyData()
        live_survey_data.to_csv(CHECKPOINT_PATH)
        print(
            "New survey data checkpoint created from {survey_data_last_checkpoint_hash} to {live_survey_data_hash}"
        )

    if checkpoint_exists and not update_required:
        # No changes necessary. View doesn't change and checkpoint can be left as is
        pass


def get_all_survey_data() -> pd.DataFrame:
    """

    """
    live_survey_data = run_sql_select_query(f"{AllSurveyData_QRY} ORDER BY UserId")

    run_maintenence_on_vw_AllSurveyData(live_survey_data)

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
    cur = CONN.execute(qry)
    cur.close()


@provide_db_connection
def create_vw_AllSurveyData(connection=None):
    """
    @provide_db_connection provides db connection object
    and closes it after the function completes
    """
    cur = CONN.execute(create_vw_AllSurveyData_qry)
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
