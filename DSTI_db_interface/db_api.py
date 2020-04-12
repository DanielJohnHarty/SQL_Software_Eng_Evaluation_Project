# Standard library imports
import configparser
import hashlib
import os

# Local Imports
from .db_connection import provide_db_connection

# External library imports
import pandas as pd
import pyodbc

# EXCEPTIONS
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


# SHARED VARIABLES

CHECKPOINT_PATH = os.path.join(
    os.path.join(os.path.dirname(__file__)), "data", "survey_data_last_checkpoint.txt",
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

# FUNCTIONS
def is_permitted_query(qry:str)-> bool:
    """
    Returns False if any flag from the 
    non_permitted_query_flags iterable are present
    in the passed query
    """
    non_permitted_query_flags = \
        ("update", "drop", "delete", "create", "alter")

    qry = qry.lower()

    no_flags = not any(
        [name in qry for name in non_permitted_query_flags]
    )

    non_empty_qry = qry is not None and qry != ""
    permitted_qry = no_flags and non_empty_qry
    return permitted_qry


@provide_db_connection
def run_sql_select_query(sql_query=None, connection=None):
    """
    Runs passed query against database using connection object.

    @provide_db_connection provides the connection object.
    """
    if not is_permitted_query(sql_query):
        raise NonPermittedQuery

    elif sql_query and connection:
        df = pd.read_sql(sql_query, connection)
        return df


def create_checkpoint_file():
    """
    The checkpoint file at CHECKPOINT_PATH
    may not exist if its the 1st time the 
    code is run or it has been removed.

    This function creates teh file but with
    nothing inside.
    """
    with open(CHECKPOINT_PATH, "w") as file:
        # Only create file, don't write anything
        pass


def get_checkpoint_hash():
    """
    Reads the hash representing the most recent
    contents of vw_AllSurveyData, from a local 
    CHECKPOINT_PATH and returns it to the caller.

    If the CHECKPOINT_PATH doesn't exist, a blank file is 
    created and None is returned.
    """

    checkpoint_hash = None
    # Create checkpoint file if one isn't found
    if not os.path.exists(CHECKPOINT_PATH):
        create_checkpoint_file()

    with open(CHECKPOINT_PATH, "r") as file:
        checkpoint_hash = file.read()

    return checkpoint_hash


def update_vw_AllSurveyData_if_obsolete(live_survey_data: pd.DataFrame) -> bool:
    """
    live_survey_data is a dataframe
    containing the results of the query
    'SELECT * from vw_AllSurveyData'.
    
    This function compares the hash of this df
    with that stored in a local checkpoint file,
    and takes the necessary actions to update 
    vw_AllSurveyData if it is obsolete.
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

    # Print action taken for the user to conveniently see
    stdout_vw_AllSurveyData_actions(obsolete, checkpoint_hash)


def stdout_vw_AllSurveyData_actions(obsolete, checkpoint_hash):
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
    """
    Writes the passed hash to the checkpoint file at
    CHECKPOINT_PATH. Destroys any pre-existing data
    in the file
    """
    if not os.path.exists(CHECKPOINT_PATH):
        create_checkpoint_file()

    # Record new checkpoint_hash
    with open(CHECKPOINT_PATH, "w") as file:
        file.write(live_survey_data_hash)


def get_all_survey_data() -> pd.DataFrame:
    """
    Querys database and for specific result set
    AllSurveyData and initiates code to check for
    obsolecence of data in the vw_AllSurveyData view.
    """
    # Latest data from live DB tables
    live_survey_data = \
        run_sql_select_query(f"{AllSurveyData_QRY} ORDER BY UserId")

    # Run code to check if the last time this was ran, if the 
    # data has changed. If yes, the vw_AllSurveyData is updated.
    update_vw_AllSurveyData_if_obsolete(live_survey_data)

    # Return result as a Pandas DataFrame
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
