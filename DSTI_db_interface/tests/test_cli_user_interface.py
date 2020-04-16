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