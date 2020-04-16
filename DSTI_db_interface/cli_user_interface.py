# Standard Library Imports
import os
import signal
import sys


# Local Imports
import DSTI_db_interface.db_api as db

# import DSTI_db_interface.db_connection as db_conn
import DSTI_db_interface.dependency_installation as di


class UserCLI:

    APP_NAME = "DSTI_Database_Interface"
    VERSION = "0.0.1"
    LINE_LENGTH = 50
    BOLD_LINE = "=" * LINE_LENGTH
    SIMPLE_LINE = "-" * LINE_LENGTH
    SMALL_INDENT = "  "
    LARGE_INDENT = "    "
    BULLET_POINT = "->"

    def __init__(self):

        self.function_mapper = {
            "1": (self.download_all_survey_data, "Download vw_AllSurveyData"),
            "2": (self.update_vw_AllSurveyData, "Update vw_AllSurveyData"),
            "3": (self.run_select_query, "Run Custom SELECT Query"),
            "4": (self.exit, "Exit"),
        }




    def run_cli_app(self):
        self.text_intro()
        self.application_loop()
        self.exit()

    def text_intro(self):
        print("\n\n\n")
        print(
            f"{UserCLI.BOLD_LINE}\n"
            + f"{UserCLI.APP_NAME} v{UserCLI.VERSION}\n"
            + f"{UserCLI.SIMPLE_LINE}\n"
        )


    def text_outro(self):
        print(
            f"\n"
            + f"{UserCLI.BOLD_LINE}\n"
            + f"Thanks for using {UserCLI.APP_NAME} v{UserCLI.VERSION}\n"
            + f"Come back soon!\n"
            + f"{UserCLI.SIMPLE_LINE}\n"
        )

    def application_loop(self):
        self.print_display_menu_options()
        print("Select function as int e.g. type 4 to exit\n\n")
        self.display_menu_options()

        choice = input()
        while choice not in self.function_mapper:
            print(
                "That choice wasn't found.\n"
                + "The options are:\n\n"
                + self.display_menu_options()
            )

            choice = input()

        function, function_desc = self.get_function_and_desc_from_choice(choice)

        print(f"\n{function_desc} selected...\n")
        function()

    def exit(self):
        self.text_outro()
        sys.exit()

    def run_select_query(self, SELECT_query=None, save_file_path=None):
        
        query_source = None
        while not query_source:
            print(f"Choose SELECT query source:\n" + 
                f"{UserCLI.SMALL_INDENT}{UserCLI.BULLET_POINT}[1] Load SELECT query from a txt file\n" +
                f"{UserCLI.SMALL_INDENT}{UserCLI.BULLET_POINT}[2] Input SELECT query on the command line"
                )

            query_source = input()
            
            if not query_source in ['1','2']:
                print("\nI didn't quite catch that...\n")
                query_source = None


        while not SELECT_query:

            qry = ''

            if query_source == '1':
                while qry == '':
                    print("Please enter the filepath of the text file with your SELECT query")#load txt file
                    filepath = input()
                    file_exists = os.path.exists(filepath)
                    is_txtfile = filepath.endswith('.txt')
                    if file_exists and is_txtfile:
                        try:
                            with open(filepath, 'r') as file:
                                qry = file.read()
                                if not db.is_permitted_query(qry):
                                    print('Only SELECT queries are permitted. Please try again.\n\n')
                                    continue
                                else:
                                    SELECT_query = qry
                        except Exception as e:
                            print(e)
                            qry = ''



            elif query_source == '2':
                while qry == '':
                    print("\nEnter your SELECT query...")
                    qry = input()
                    if not db.is_permitted_query(qry):
                        print('Only SELECT queries are permitted. Please try again.\n\n')
                        qry == ''
                        continue
                    else:
                        SELECT_query = qry
                        break

        
            else:
                print("xxx")
        results = db.run_sql_select_query(SELECT_query)


        while not save_file_path:
            print("\nEnter a local path for saving the csv file\n")
            user_input_fullpath = input().lower()
            directory_exists = os.path.exists(os.path.dirname(user_input_fullpath))
            is_csv = user_input_fullpath.endswith(".csv")

            if directory_exists and is_csv:
                save_file_path = user_input_fullpath
                break
            else:
                print(
                    "Double check that the directory exists "
                    + "and that the target filename is valid,"
                    + ' ending with ".csv"\n'
                )
                continue
        
        results.to_csv(save_file_path)

        results_summary = f'\nQuery\n\n{SELECT_query}\n\nResults saved to\n{save_file_path}\n\n'
        print(results_summary)

        self.application_loop()


    def update_vw_AllSurveyData(self):
        db.update_vw_AllSurveyData_if_obsolete()
        print('\n')
        self.application_loop()

        self.application_loop()

    def download_all_survey_data(self, save_file_path=None):
        while not save_file_path:
            print("Enter a local path for saving the csv file\n")
            user_input_fullpath = input().lower()
            directory_exists = os.path.exists(os.path.dirname(user_input_fullpath))
            is_csv = user_input_fullpath.endswith(".csv")

            if directory_exists and is_csv:
                save_file_path = user_input_fullpath
                break
            else:
                print(
                    "Double check that the directory exists"
                    + "and that the target filename is valid,"
                    + ' ending with ".csv"\n'
                )
                continue
        
        update_view = None


        print("\nYou want to update vw_AllSurveyData too? [y/n]\n")
        while update_view is not False and update_view is not True:
            user_selection = input()
            if user_selection == "y":
                update_view = True
                print('OK, UPDATING vw_AllSurveyData...')

            elif user_selection =="n":
                update_view = False
                print('OK, NOT UPDATING vw_AllSurveyData...')

            else:
                print("\nI didn't quite get that.\nYou want to update vw_AllSurveyData too? [y/n]\n")


        print('\n')
        all_survey_data = db.get_all_survey_data(update_view=update_view)

        try:
            all_survey_data.to_csv(save_file_path)
        except Exception as e:
            print(e)

        finally:

            results_str = f'\n{UserCLI.SMALL_INDENT}{UserCLI.BULLET_POINT}' + f' AllSurveyData saved to "{save_file_path}"'

            results_str += ' without updating vw_AllSurveyData' if not update_view else ''

            print(results_str + '\n\n')

            self.application_loop()


    def print_display_menu_options(self):
        print('Choose operation:\n')
        print(self.display_menu_options())

    def get_function_and_desc_from_choice(self, choice: int):
        function, function_desc = self.function_mapper[choice]

        return function, function_desc

    def display_menu_options(self):

        disp_options_str = ""
        for option_number, func_desc_tuple in self.function_mapper.items():
            _, function_desc = func_desc_tuple[0], func_desc_tuple[1]
            disp_options_str += (
                f"{UserCLI.SMALL_INDENT}{option_number} - {function_desc}\n"
            )

        return disp_options_str
