# Standard Library Imports
import os
import sys

PROJECT_ROOT = \
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add project root to sys.path
sys.path.insert(0, PROJECT_ROOT)

# Local Imports
import DSTI_db_interface.cli_user_interface as cli_user_interface

# 3rd party packages
import pytest

# SHARED_VARIABLES
# DF_1 = pd.DataFrame({"A": 1, "B": 2, "C": 3}, index=(1, 2, 3))
# DF_2 = pd.DataFrame({"A": 2, "B": 4, "C": 6}, index=(1, 2, 3))


def test_instantiate_cli():
    """
    Test that UserCLI class exists in cli_user_interface
    """
    assert 'UserCLI' in cli_user_interface.__dict__


def test_project_root_in_path():
    """
    Ensure that the project root has been correctly added
    to the Python import path sys.path
    """
    assert PROJECT_ROOT in sys.path