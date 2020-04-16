# Standard Library Imports
import functools
import os
import signal
import sys


# Local Imports
import DSTI_db_interface.db_api as db

# import DSTI_db_interface.db_connection as db_conn
import DSTI_db_interface.dependency_installation as di
import DSTI_db_interface.file_utilities as futils


# DECORATORS
def _delineate_stdout(func):
    """
    Decorator which prints a line to printed output
    before and after any function or ,ethod it decorates.

    Used to help separate output from
    different function/ method calles.
    """

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        print(f"{UserCLI.SIMPLE_LINE}\n")
        func(*args, **kwargs)

    return wrapped_func


class UserCLI:
    """
    Class to instantiate a CLI interface
    for DSTI database interface code
    """

    APP_NAME = "DSTI_Database_Interface"
    VERSION = "0.0.1"
    LINE_LENGTH = 50
    BOLD_LINE = "=" * LINE_LENGTH
    SIMPLE_LINE = "-" * LINE_LENGTH
    SMALL_INDENT = "  "
    LARGE_INDENT = "    "
    BULLET_POINT = "->"

    def __init__(self):

        print("\n\n\n")  # Clear some space in the stdout
        self.feature_map = self.get_cli_feature_map()

    def get_cli_feature_map(self) -> dict:
        """
        The features presented to the user as menu options
        when using this cli are defined in the function_mapper
        dict in this function, and returned to 
        the caller as 3 iterables: index, function and description.
        """

        # index :(function, function_description)
        function_mapper = {
            "1": (self.download_all_survey_data, "Download vw_AllSurveyData"),
            "2": (self.update_vw_AllSurveyData, "Update vw_AllSurveyData"),
            "3": (self.run_select_query, "Run Custom SELECT Query"),
            "4": (self.exit, "Exit"),
        }

        return function_mapper

    def get_cli_features_options_and_descriptions(self) -> (list, list):
        """
        Helper function to pull out 2 lists from the self.feature_map
        attribute.
        """
        feature_indicies = self.feature_map.keys()
        feature_descriptions = [v[1] for v in self.feature_map.values()]

        return feature_indicies, feature_descriptions

    def get_user_input(self, option_index, option_description):
        """
        Prints valid inputs and safely gets user selection
        """
        user_selection = None
        while not user_selection:
            for i, desc in zip(option_index, option_description):
                print(f"{UserCLI.SMALL_INDENT}{i} -> {desc}")

            print("\n")
            user_input = input()

            if not user_input in option_index:
                print(
                    f"\n{UserCLI.SMALL_INDENT} Sorry, I didn't quite catch that...\n Your options are:\n"
                )
                user_selection = None
            else:
                user_selection = user_input

        return user_selection

    def run_cli_app(self):
        """
        Method used to separate class instantiation from
        entering in the user CLI loop
        """
        self.text_intro()
        self.application_cycle()

    def text_intro(self):
        """
        First text printed to stdout
        when using a CLI instance
        """
        print("\n\n")
        print(f"{UserCLI.BOLD_LINE}\n" + f"{UserCLI.APP_NAME} v{UserCLI.VERSION}")

    def text_outro(self):
        """
        Last text printed to stdout
        when using a CLI instance
        """
        print(
            f"\n"
            + f"{UserCLI.BOLD_LINE}\n"
            + f"Thanks for using {UserCLI.APP_NAME} v{UserCLI.VERSION}\n"
            + f"Come back soon!\n"
            + f"{UserCLI.SIMPLE_LINE}\n"
        )

    @_delineate_stdout
    def application_cycle(self):
        """
        One iteration though the cycle of selecting
        a feature and executing it.
        """
        print("Select function as int e.g. type 4 to exit\n")
        opts, descs = self.get_cli_features_options_and_descriptions()
        choice = self.get_user_input(opts, descs)
        function, function_desc = self.get_function_and_desc_from_choice(choice)
        print(f"\n{function_desc} selected...\n")
        function()

    def exit(self):
        """
        Shutdown steps of cli app
        """
        self.text_outro()
        sys.exit()

    @_delineate_stdout
    def run_select_query(self, SELECT_query=None, save_file_path=None):
        """
        Runs a custom SELECT query from the user
        against the db, saving the results to a local csv file.

        Non SELECT queries are not executed.
        """
        while not SELECT_query:

            print(f"Choose SELECT query source:\n")

            opts = ["1", "2"]
            descs = [
                f"Load SELECT query from a txt file",
                f"Input SELECT query on the command line",
            ]

            user_selection = self.get_user_input(opts, descs)

            if user_selection == "1":  # Load from text file

                print("\nOK, loading query from local text file...\n")
                query_txt_filepath = futils.get_user_text_file()
                qry = futils.get_sql_from_text_file_as_text(query_txt_filepath)

                if db.is_non_empty_select_query(qry):
                    SELECT_query = qry
                else:
                    print(f"\nYour query doesn't seem to be quite right:\n")
                    print(qry + "\n")

            if user_selection == "2":  # Write query in cli
                print("\nOK, enter your query on to a single line:\n")
                qry = input()

                # A permitted query may still be incorrect SQL (change to is_non_empty_select_query)
                if db.is_non_empty_select_query(qry):
                    SELECT_query = qry

                else:
                    print(f"\nYour query doesn't seem to be quite right:\n")
                    print(qry + "\n")

        try:

            results = db.run_sql_select_query(SELECT_query)

            if any(results):
                save_file_path = futils.get_target_filepath_to_save(".csv")

                results.to_csv(save_file_path)

                results_summary = f"\nExecuted Query:\n\n{SELECT_query}\n\nResults saved to\n{save_file_path}\n"
                print(results_summary)
            else:
                results_summary = f"\nSuccessful query but no results retrieved\n"

                print(results_summary)

        except Exception as e:
            print("The following error occured:\n")
            print(e)
            print("Sorry about it.")

        self.application_cycle()

    @_delineate_stdout
    def update_vw_AllSurveyData(self):
        """
        The vw_AllSurveyData need manually updated.

        This function takes the latest AllSurveyData from
        live tables and updates the vw_AllSurveyData if the
        live results hash is differen,t to the last persisted
        results hash.
        """

        db.update_vw_AllSurveyData_if_obsolete()
        print("\n")
        self.application_cycle()

        self.application_cycle()

    @_delineate_stdout
    def download_all_survey_data(self, save_file_path=None):
        """
        Queries the latest AllSurveyData and saves the results
        to a local csv.

        Optionally updates vw_AllSurveyData (user input requested)
        """
        save_file_path = futils.get_target_filepath_to_save("csv")

        print("\nYou want to update vw_AllSurveyData too? [y/n]\n")

        update_view = self.get_user_input(
            ["y", "n"], ["Yes, update vw_AllSurveyData", "No, don't bother"]
        )

        update_view = True if update_view == "y" else False

        all_survey_data = db.get_all_survey_data(update_view=update_view)

        try:
            all_survey_data.to_csv(save_file_path)
        except Exception as e:
            print(e)

        finally:

            results_str = (
                f"\n{UserCLI.SMALL_INDENT}{UserCLI.BULLET_POINT}"
                + f' AllSurveyData saved to "{save_file_path}"'
            )

            results_str += (
                " without updating vw_AllSurveyData" if not update_view else ""
            )

            print(results_str + "\n\n")

            self.application_cycle()

    def get_function_and_desc_from_choice(self, choice: str):
        function, function_desc = self.feature_map[choice]
        return function, function_desc
