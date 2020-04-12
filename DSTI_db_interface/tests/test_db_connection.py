# Standard Library Imports
import os
import sys

PROJECT_ROOT = \
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add project root to sys.path
sys.path.insert(0, PROJECT_ROOT)

# Local Imports
import DSTI_db_interface.db_connection as dbconn

# 3rd party packages
import pyodbc


def test_config_ini_file_present():
    config_file_pth = os.path.join(PROJECT_ROOT, 'config.ini')
    assert os.path.exists(config_file_pth)

def test_get_db_connect_returns_string():
    conn_str = dbconn.get_db_connection_string()
    assert isinstance(conn_str, str)

def test_get_db_connection_returns_pyodbc_Connection():
    conn = dbconn.get_db_connection()
    assert isinstance(conn, pyodbc.Connection)