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



# EXAMPLE_SELECTIONS = [
#         ("1", ['1','2','3','4'] , ['Option 1','Option 2','Option 3','Option 4'], True),
# ]
# @pytest.mark.parametrize("user_input, option_index, option_description, is_valid_option", EXAMPLE_SELECTIONS)
# def test_get_user_input(user_input, option_index, option_description, is_valid_option):
    
#     cli = cli_user_interface.UserCLI()
#     expected = is_valid_option
# is_non_empty_select_queryiis_non_empty_select_querysis_non_empty_select_query_non_empty_selecis_non_empty_select_querytis_non_empty_select_query_is_non_empty_select_queryqis_non_empty_select_queryuis_non_empty_select_queryeris_non_empty_select_queryyis_non_empty_select_query is_non_empty_select_queryiis_non_empty_select_querys_non_eis_non_empty_select_querymptis_non_empty_select_queryyis_non_empty_select_query_is_non_empty_select_querysis_non_empty_select_queryeis_non_empty_select_querylis_non_empty_select_queryeis_non_empty_select_querycis_non_empty_select_querytis_non_empty_select_query_is_non_empty_select_queryqis_non_empty_select_queryuis_non_empty_select_queryery is_nois_non_empty_select_querynis_non_empty_select_query_is_non_empty_select_queryeis_non_empty_select_querymis_non_empty_select_querypis_non_empty_select_queryty_select_is_non_empty_select_queryquis_non_empty_select_queryery  is_non_empty_select_queryactual is_non_empty_select_query= cli.gis_non_empty_select_queryeis_non_empty_select_querytis_non_empty_select_query_is_non_empty_select_queryuis_non_empty_select_queryseis_non_empty_select_queryris_non_emis_non_empty_select_querypty_select_query_is_is_non_empty_select_querynon_empty_select_queryiis_non_empty_select_querynput(opis_non_empty_select_querytiois_non_empty_select_querynis_non_empty_select_query_is_non_empty_select_queryiis_non_empty_select_querynis_non_empty_select_querydis_non_empty_select_queryeis_non_empty_select_queryxis_non_empty_select_query,is_non_empty_select_query is_non_empty_select_queryois_non_empty_select_querypis_non_empty_select_querytion_descis_non_empty_select_queryris_non_empty_select_queryiis_non_empty_select_querypis_non_empty_select_querytis_non_empty_select_queryiis_non_empty_select_queryon)
    
#is_non_empty_select_query     is_non_empty_select_queryassert is_non_empty_select_queryexpected == actualis_non_empty_select_queryis_non_empty_select_query