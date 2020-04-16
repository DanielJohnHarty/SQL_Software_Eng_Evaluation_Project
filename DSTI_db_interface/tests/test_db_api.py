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

# SHARED_VARIABLES
DF_1 = pd.DataFrame({"A": 1, "B": 2, "C": 3}, index=(1, 2, 3))
DF_2 = pd.DataFrame({"A": 2, "B": 4, "C": 6}, index=(1, 2, 3))

EXAMPLE_QUERIES = [
    ("SELECT * FROM tbl UPDATE WHERE id=1", False),
    ("DROP TABLE [IF EXISTS]", False),
    ("DELETE FROM table_name WHERE condition", False),
    ("SELECT * FROM tbl UPDATE WHERE id=1", False),
    ("ALTER TABLE table_name\nADD column_name datatype;", False),
]


@pytest.mark.parametrize("qry, is_permitted", EXAMPLE_QUERIES)
def test_update_query_raises_NonPermittedQuery(qry, is_permitted):
    """
    Test passes if the custom exception
    NonPermittedQuery is raised when passing a 
    qry flagged as 'is_permitted=False'
    """
    if not is_permitted:
        with pytest.raises(db.NonPermittedQuery):
            db.run_sql_select_query(qry)


@pytest.mark.parametrize("qry, is_permitted", EXAMPLE_QUERIES)
def test_NonPermittedQuery_status(qry, is_permitted):
    """
    Test that the is_permitted function
    returns the expected TRUE/FALSE
    """
    expected = is_permitted
    actual = db.is_non_empty_select_query(qry)
    assert expected == actual


@provide_db_connection
def test_run_sql_select_query_returns_df(connection=None):
    """
    @provide_db_connection provides the connection object
    and closes it after the function call is complete
    """

    table = "[dbo].[User]"
    qry = f"SELECT * FROM {table}"

    df = pd.read_sql(qry, connection)
    assert isinstance(df, pd.DataFrame)


def test_project_root_in_path():
    """
    Ensure that the project root has been correctly added
    to the Python import path sys.path
    """
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    assert PROJECT_ROOT in sys.path
