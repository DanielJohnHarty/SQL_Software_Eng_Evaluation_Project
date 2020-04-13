# Standard library imports
import os

# Local Imports
from . import db_api as db
from .db_connection import provide_db_connection

# External library imports
import pandas as pd

# EXCEPTIONS
class DynamicQueryMissingParameters(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "DynamicQueryMissingParameters, {0} ".format(self.message)
        else:
            return """Additional parameters are needed to
                   generate the requested query. Running an
                   incomplete query against the database can
                   have unexpected results and cause unecessary
                   storage and performance costs."""


# DYNAMIC QUERY FUNCTIONS


def get_strQueryTemplateForAnswerColumn(survey_id=None, question_id=None) -> str:
    """
    Builds and returns an SQL query string using the passed parameters.

    This query is used to add a column to AllSurveyData representing the
    answer to a particular question.
    """
    if not survey_id or not question_id:
        raise DynamicQueryMissingParameters

    return f"""
			,COALESCE(
				(
					SELECT a.Answer_Value
					FROM Answer as a
					WHERE
						a.UserId = u.UserId
						AND a.SurveyId = {survey_id}
						AND a.QuestionId = {question_id}
				), -1) AS ANS_Q{question_id}
            """


def get_strQueryTemplateForNullColumn(question_id=None) -> str:
    """
    Builds and returns an SQL query string using the passed parameters.

    This query is used to add a column to AllSurveyData representing that
    this particular question has not been asked or has not been answered.
    """
    if not question_id:
        raise DynamicQueryMissingParameters

    return f"""
                , NULL AS ANS_Q{question_id}
            """


def get_strQueryTemplateOuterUnionQuery(
    survey_id=None, dynamic_question_answers=None
) -> str:
    """
    Builds and returns an SQL query string 
    using the passed parameters.

    This query is selects answers to the questions
    which a user has been asked.
    """
    if not survey_id or not dynamic_question_answers:
        raise DynamicQueryMissingParameters

    return f"""SELECT
					UserId
					, {survey_id} as SurveyId
					  {dynamic_question_answers}
			FROM
				[User] as u
			WHERE EXISTS
			(
					SELECT *
					FROM Answer as a
					WHERE u.UserId = a.UserId
					AND a.SurveyId = {survey_id} 
			)"""


@provide_db_connection
def get_survey_ids(connection=None) -> list:
    qry = "SELECT SurveyId FROM Survey ORDER BY SurveyId"
    surveyIds = db.run_sql_select_query(qry)
    surveyIds_as_list = surveyIds["SurveyId"].to_list()
    return surveyIds_as_list


@provide_db_connection
def get_question_ids(connection=None) -> list:
    qry = "SELECT QuestionId FROM Question ORDER BY QuestionId"
    questionIds = db.run_sql_select_query(qry)
    questionIds_as_list = questionIds["QuestionId"].to_list()
    return questionIds_as_list


# currentQuestionCursor
def get_questions_in_survey_qry(survey_id=None) -> str:
    """
    Builds and returns an SQL query string
    using the passed parameters.

    This query is used to find all 
    questions present in a particular survey
    """
    if not survey_id:
        raise DynamicQueryMissingParameters

    return f"""SELECT *
                FROM
                (
                    SELECT
                        SurveyId,
                        QuestionId,
                        1 as InSurvey
                    FROM
                        SurveyStructure
                    WHERE
                        SurveyId = {survey_id}
                    UNION
                    SELECT 
                        {survey_id} as SurveyId,
                        Q.QuestionId,
                        0 as InSurvey
                    FROM
                        Question as Q
                    WHERE NOT EXISTS
                    (
                        SELECT *
                        FROM SurveyStructure as S
                        WHERE S.SurveyId = {survey_id} AND S.QuestionId = Q.QuestionId
                    )
                ) as t
                ORDER BY QuestionId"""


def get_dynamic_query_to_update_vw_AllSurveyData() -> str:
    """
    This function build a dynamic query string, based on
    the contents of live database tables.

    The goal is to build a select function which can be used
    to create a view with the following format:

    +--------+----------+-------+-----+-------+
    | UserId | SurveyId | ANS_1 | ... | ANS_N |
    +--------+----------+-------+-----+-------+
    |    _   |     _    |   _   | ... |   _   |
    +--------+----------+-------+-----+-------+
    |    _   |     _    |   _   | ... |   _   |
    +--------+----------+-------+-----+-------+
    |    _   |     _    |   _   | ... |   _   |
    +--------+----------+-------+-----+-------+

    """

    # Appended to during the function
    # and finally returned to caller
    wip_query = ""

    # The latest set of all surveys from
    # the Survey table
    all_survey_ids = get_survey_ids()

    # OUTER LOOP
    for survey_id in all_survey_ids:

        # New questions and answers may have been
        # added to the live databse tables so
        # we create a dynamic string to append
        # a column for each question with a value of
        # NULL (question not in survey),
        # -1 (question not answered) or the recorded answer
        answer_columns_qry = ""

        # INNER LOOP
        """
        Iterate over questions, adding
        the appropriate dynamic query part 
        for this row depending on whether 
        the question was part of the current survey.
        """
        questions_in_survey = get_questions_in_survey(survey_id)

        """
        questions_in_survey looks like this:
            +----------+------------+----------+
            | SurveyId | QuestionId | InSurvey |
            +----------+------------+----------+
            |     1    |      1     |     1    | # Question 1 in Survey 1
            +----------+------------+----------+
            |     1    |      2     |     0    | # Question 2 not in Survey 1
            +----------+------------+----------+
            |     1    |      3     |     1    |
            +----------+------------+----------+
        """
        for row in questions_in_survey.itertuples():
            question_id = row.QuestionId
            if row.InSurvey == 0:
                # Question not in survey so add NULL as column
                answer_columns_qry += get_strQueryTemplateForNullColumn(question_id)

            else:
                # Question is in survey so add the
                # value based on the users answer
                answer_columns_qry += get_strQueryTemplateForAnswerColumn(
                    survey_id, question_id
                )

        # Before moving on to next survey, add
        # this survey to the final query string
        current_survey_select_qry = get_strQueryTemplateOuterUnionQuery(
            survey_id=survey_id, dynamic_question_answers=answer_columns_qry
        )

        wip_query += f"{current_survey_select_qry} UNION "

    # Remove final unecessary ' UNION '
    final_query_string = wip_query[:-7]

    return final_query_string


def get_questions_in_survey(survey_id) -> pd.DataFrame:
    questions_in_survey_qry = get_questions_in_survey_qry(survey_id)

    questions_in_survey = db.run_sql_select_query(questions_in_survey_qry)

    return questions_in_survey
