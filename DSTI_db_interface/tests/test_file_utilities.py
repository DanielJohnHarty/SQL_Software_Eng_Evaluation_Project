# Standard Library Imports
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add project root to sys.path
sys.path.insert(0, PROJECT_ROOT)

# Local Imports
import DSTI_db_interface.file_utilities as futil

# 3rd party packages
import pytest

# SHARED_VARIABLES

EXAMPLE_FILENAMES = [
    ("test_54.csv", True),
    ("test_54.txt", False),
    ("query results.csv", False),
    ("my-file-namecsv", False),
    ("my_file_namecsv", False),
    ("filènamewithaccent1.csv", False),
    ("filenamewithàccent2.csv", False),
    ("filenamewithaccént3.csv", False),
    ("filenamewithâccent4.csv", False),
    ("filenamewithùccent5.csv", False),
    ("filênamewithaccent6.csv", False),
]


@pytest.mark.parametrize("filename, is_permitted", EXAMPLE_FILENAMES)
def test_permitted_file_name(filename, is_permitted):
    """
    Test passes if the custom exception
    NonPermittedQuery is raised when passing a 
    qry flagged as 'is_permitted=False'
    """
    expected = is_permitted
    actual = futil.is_permitted_filename(filename)
    assert expected == actual
