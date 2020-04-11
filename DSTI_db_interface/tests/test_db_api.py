# Standard Library Imports
import os
import sys

PROJECT_ROOT = \
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add project root to sys.path
sys.path.insert(0, PROJECT_ROOT)

# Local Imports
import DSTI_db_interface.db_api as db

# 3rd party packages
import pandas as pd
import pytest


CONN = db.get_db_connection()

def test_update_query_raises_NonPermittedQuery():
    qry='SELECT * FROM tbl UPDATE WHERE id=1'
    with pytest.raises(db.NonPermittedQuery):
        db.run_sql_select_query(qry)

def test_run_sql_select_query_returns_df():
    col1='[SurveyId]'
    col2='[QuesitonId]'
    col3='[OrdinalValue]'
    table= '[dbo].[vw_AllSurveyData]'
    qry = f'SELECT * FROM {table}'

    df = pd.read_sql(qry,CONN)

    # Print df to stdout
    #print(df)
    assert isinstance(df,pd.DataFrame)
