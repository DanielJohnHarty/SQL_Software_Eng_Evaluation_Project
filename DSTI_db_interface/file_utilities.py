# Standard library imports
import os
import re


def is_permitted_filename(filename: str) -> bool:
    """
    Returns True if passed filename is compatible 
    with permitted_filename_regex_pattern (defined below):
    """
    # Any patterns of characters a-z, _ or 0-9
    permitted_filename_regex_pattern = r"^[A-Za-z0-9_.]+$"

    file_extention_ok = filename.lower().endswith(".csv")

    filename_characterset_ok = re.match(permitted_filename_regex_pattern, filename)

    if file_extention_ok and filename_characterset_ok:
        result = True
    else:
        result = False

    return result


def get_user_text_file():
    """
    Get a text file filepath from the user
    and validate it
    """
    filepath = None

    while not filepath:
        print("\nWhere is your file?\n")

        filepath = input()
        is_valid_path = os.path.exists(filepath)
        is_valid_file_type = filepath.lower().endswith(".txt")

        if is_valid_path and is_valid_file_type:
            return filepath
        else:
            print("Sorry, that filepath doesn't seem quite right...\n")
            print(f"Make sure the filepath is correct and that it's a '.txt' file\n")
            filepath = None


def get_sql_from_text_file_as_text(filepath):
    with open(filepath, "r") as file:
        sql = file.read()
        return sql


def get_target_filepath_to_save(target_file_type):
    """
    Request a target filepath from the user to save a file locally
    """
    filepath = None

    while not filepath:
        print("\nPlease enter a full path and csv filename to save the results to...\n")

        filepath = input()
        is_valid_path = is_valid_write_filepath(filepath)
        is_valid_file_type = filepath.lower().endswith(target_file_type)

        if is_valid_path and is_valid_file_type:
            return filepath
        else:
            print("Sorry, that filepath doesn't seem quite right...\n")
            print(
                f"Make sure the directory exists and it's a {target_file_type} file\n"
            )
            filepath = None


def is_valid_write_filepath(filepath):
    """
    Checks if it is possible to write to the passed filepath.
    """
    target_dir = os.path.dirname(filepath)
    target_dir_exists = os.path.exists(target_dir)
    return target_dir_exists


def is_valid_read_filepath(filepath, file_type=".txt"):
    """
    Checks if it is possible to read from
    the passed filepath.
    """
    file_type_ok = filepath.endswith(file_type)
    target_path_exists = os.path.exists(filepath)

    return file_type_ok and target_path_exists
