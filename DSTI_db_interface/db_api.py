# Standard library imports
import configparser

# Local Imports
from .db_connection import get_db_connection

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
        #print('calling str')
        if self.message:
            return 'NonPermittedQuery, {0} '.format(self.message)
        else:
            return 'NonPermittedQuery has been raised'

CONN = get_db_connection()

def is_permitted_query(sql_query):
    qry = sql_query.lower()
    select_only_qry = not any(
        [name in qry for name in ('update','drop','delete', 'create')]
    )
    non_empty_qry = qry is not None and qry != ''
    permitted_qry = select_only_qry and non_empty_qry
    return permitted_qry

def run_sql_select_query(sql_query, connection=CONN):
    """
    Runs passed query against database using CONN object
    """

    if not is_permitted_query(sql_query):
        raise NonPermittedQuery
    else:
        df = pd.read_sql(query, connection)
        return df


def get_all_survey_data(survey_id):
    """
    Returns a dynamic SQL query string
    """
    pass


def trg_refreshSurveyView():
    """
    Updates [dbo].[vw_AllSurveyData] view with latest data (always fresh)
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


