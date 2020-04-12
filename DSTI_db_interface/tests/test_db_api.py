# Standard Library Imports
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add project root to sys.path
sys.path.insert(0, PROJECT_ROOT)

# Local Imports
import DSTI_db_interface.db_api as db
from DSTI_db_interface.db_connection import provide_db_connection

# 3rd party packages
import pandas as pd
import pytest

DF_1 = pd.DataFrame({"A": 1, "B": 2, "C": 3}, index=(1, 2, 3))
DF_2 = pd.DataFrame({"A": 2, "B": 4, "C": 6}, index=(1, 2, 3))
#CONN = db.get_db_connection()

example_queries = [
    ("SELECT * FROM tbl UPDATE WHERE id=1", False),
    ("DROP TABLE [IF EXISTS]", False),
    ("DELETE FROM table_name WHERE condition", False),
    ("SELECT * FROM tbl UPDATE WHERE id=1", False),
    ("ALTER TABLE table_name\nADD column_name datatype;", False),
]


@pytest.mark.parametrize("qry, is_permitted", example_queries)
def test_update_query_raises_NonPermittedQuery(qry, is_permitted):
    if not is_permitted:
        with pytest.raises(db.NonPermittedQuery):
            db.run_sql_select_query(qry)


@pytest.mark.parametrize("qry, is_permitted", example_queries)
def test_NonPermittedQuery_status(qry, is_permitted):
    expected = is_permitted
    actual = db.is_permitted_query(qry)
    assert expected == actual



@provide_db_connection
def test_run_sql_select_query_returns_df(connection=None):
    """
    @provide_db_connection provides the connection object
    and closes it after the function call is complete
    """
    table = "[dbo].[vw_AllSurveyData]"
    qry = f"SELECT * FROM {table}"

    df = pd.read_sql(qry, connection)
    assert isinstance(df, pd.DataFrame)

test_run_sql_select_query_returns_df() 