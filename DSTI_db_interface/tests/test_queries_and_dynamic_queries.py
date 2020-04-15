# Standard Library Imports
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add project root to sys.path
sys.path.insert(0, PROJECT_ROOT)

# Local Imports
# local import part of test suite
import DSTI_db_interface.queries_and_dynamic_queries as q

# 3rd Party Imports
import pytest

# SHARED VARIABLES
test_survey_id = 1
test_question_id = 1
test_dynamic_question_answers = 1

dynamic_query_calls = [
    (q.get_strQueryTemplateForAnswerColumn, [test_survey_id, test_question_id]),
    (q.get_strQueryTemplateForNullColumn, [test_question_id]),
    (
        q.get_strQueryTemplateOuterUnionQuery,
        [test_survey_id, test_dynamic_question_answers],
    ),
    (q.get_questions_in_survey_qry, [test_survey_id]),
]


@pytest.mark.parametrize("func, parameters", dynamic_query_calls)
def test_dynamic_query_fails_without_parameters(func, parameters):
    """
    Tests fail if proper exceptions are not raised when 
    missing or incomplete arguments are passed to dynamic
    string generation function
    """
    with pytest.raises(q.DynamicQueryMissingParameters):
        func()


@pytest.mark.parametrize("func, parameters", dynamic_query_calls)
def test_dynamic_query_returns_string(func, parameters):
    """
    Tests that the dynamic queries passed as parameters return strings
    """
    expected = True
    actual = isinstance(func(*parameters), str)
    assert expected == actual


functions_returning_lists = [(q.get_survey_ids), (q.get_question_ids)]


@pytest.mark.parametrize("func", functions_returning_lists)
def test_get_survey_ids_returns_list(func):
    returned_object = func()
    assert isinstance(returned_object, list)

def test_project_root_in_path():
    """
    Ensure that the project root has been correctly added
    to the Python import path sys.path
    """
    assert PROJECT_ROOT in sys.path