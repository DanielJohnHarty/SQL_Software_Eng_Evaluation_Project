# Standard Library Imports
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add project root to sys.path
sys.path.insert(0, PROJECT_ROOT)

# Local Imports
import DSTI_db_interface.db_connection as dbconn

# 3rd party packages
import pyodbc


def test_config_ini_file_present():
    """
    Tests that config.ini is present in the project root
    where it needs to be.
    """
    config_file_pth = os.path.join(PROJECT_ROOT, "config.ini")
    assert os.path.exists(config_file_pth)


def test_get_db_connect_returns_string():
    """
    Tests that the get_db_connection_string function
    returns a simple string and not an object.
    """
    conn_str = dbconn.get_db_connection_string()
    assert isinstance(conn_str, str)


def test_get_db_connection_returns_pyodbc_Connection():
    """
    Asserts that the object type used to connect with
    the database is a pyodbc.Connection object
    """
    conn = dbconn.get_db_connection()
    assert isinstance(conn, pyodbc.Connection)


def test_project_root_in_path():
    """
    Ensure that the project root has been correctly added
    to the Python import path sys.path
    """
    assert PROJECT_ROOT in sys.path
