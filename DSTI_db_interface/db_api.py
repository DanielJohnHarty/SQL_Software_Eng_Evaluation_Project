# Standard library imports
import configparser

# Local Imports
from .db_connection import get_db_connection

# External library imports
import pandas as pd
import pyodbc


CONN = get_db_connection()


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


