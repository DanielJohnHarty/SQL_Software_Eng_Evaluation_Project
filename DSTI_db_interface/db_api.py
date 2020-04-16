# Standard library imports
import configparser
import hashlib
import os

# Local Imports
from .db_connection import provide_db_connection
from .queries_and_dynamic_queries import get_dynamic_query_to_update_vw_AllSurveyData

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
        if self.message:
            return "NonPermittedQuery, {0} ".format(self.message)
        else:
            return "NonPermittedQuery has been raised"


# SHARED VARIABLES

CHECKPOINT_PATH = os.path.join(
    os.path.join(os.path.dirname(__file__)), "data", "survey_data_last_checkpoint.txt"
)


# FUNCTIONS
def is_non_empty_select_query(qry: str) -> bool:
    """
    Returns False if any flag from the 
    non_permitted_query_flags iterable are present
    in the passed query
    """
    non_permitted_query_flags = ("update", "drop table", "delete", "create table", "alter table")

    qry = qry.lower()

    no_flags = not any([name in qry for name in non_permitted_query_flags])

    non_empty_qry = qry is not None and qry != ""
    permitted_qry = no_flags and non_empty_qry
    return permitted_qry


@provide_db_connection
def run_sql_select_query(sql_query=None, connection=None) -> pd.DataFrame:
    """
    Runs passed query against database using connection object.
    It will not run any destructive or modicative qry,
    instead raising a NonPermittedQuery exception.

    @provide_db_connection provides the connection object.

    Returns a pandas dataframe.
    """
    if not is_non_empty_select_query(sql_query):
        raise NonPermittedQuery

    elif sql_query and connection:
        try:
            df = pd.read_sql(sql_query, connection)
            return df
        except Exception as e:
            print(f"There seems to be a problem. The query wasn't executed correctly\n")
            print(f"The following error occured:\n{e}\n")
            print("Sorry about it...")



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


def update_vw_AllSurveyData_if_obsolete(live_survey_data: pd.DataFrame = None) -> bool:
    """
    live_survey_data is the result of
     a call to get_all_survey_data()

    This function compares the hash the
    last dataset (stored in a checkpoint file locally)
    to the latest. 

    In case of any difference, a new checkpoint is created
    and the view is updated.
    """

    if live_survey_data is None:
        live_survey_data = get_all_survey_data(update_view=False)

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
    stdout_vw_AllSurveyData_actions(obsolete, checkpoint_hash, live_survey_data_hash)


def stdout_vw_AllSurveyData_actions(
    obsolete, checkpoint_hash, live_survey_data_hash
) -> str:
    if obsolete:
        print(
            f"vw_AllSurveyData data obsolete. Updating checkpoint: {checkpoint_hash} -> {live_survey_data_hash}"
        )
    elif not checkpoint_hash:
        print(
            f"First checkpoint recorded using current vw_AllSurveyData data: {live_survey_data_hash}"
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


def get_all_survey_data(update_view=True) -> pd.DataFrame:
    """
    Querys database and for specific result set
    AllSurveyData.

    By default, vw_AllSurveyData is updated but can be
    skipped with update_view=False.
    """
    # Latest data from live DB tables
    qry = get_dynamic_query_to_update_vw_AllSurveyData()

    # ORDER BY essential to ensure same hash even if
    # the order of the result set is different
    live_survey_data = run_sql_select_query(f"{qry} ORDER BY UserId")

    if update_view:
        update_vw_AllSurveyData_if_obsolete(live_survey_data=live_survey_data)

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
def drop_vw_AllSurveyData(connection=None) -> None:
    """
    @provide_db_connection provides db connection object
    and closes it after the function completes
    """
    qry = "DROP VIEW IF EXISTS [dbo].[vw_AllSurveyData]"
    cur = connection.execute(qry)
    cur.commit()
    cur.close()


@provide_db_connection
def create_vw_AllSurveyData(connection=None) -> None:
    """
    @provide_db_connection provides db connection object
    and closes it after the function completes
    """
    qry = get_dynamic_query_to_update_vw_AllSurveyData()
    cur = connection.execute(qry)
    cur.commit()
    cur.close()
