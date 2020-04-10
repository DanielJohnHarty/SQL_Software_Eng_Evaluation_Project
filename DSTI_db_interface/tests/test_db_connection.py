# Standard Library Imports
import os
import sys

PROJECT_ROOT = \
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add project root to sys.path
sys.path.insert(0, PROJECT_ROOT)

# Local Imports
import DSTI_db_interface.db_connection as dbconn


def test_get_dbconnection_string():
    conn_str = dbconn.get_db_connection_string()
    assert isinstance(conn_str, str)