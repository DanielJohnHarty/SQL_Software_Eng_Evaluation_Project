# Standard library imports
import configparser
import functools
import os

# Local Imports

# External library imports
import pyodbc

# EXCEPTIONS
class DBConnectionFailed(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "DBConnectionFailed, {0} ".format(self.message)
        else:
            return """Ensure that all connection parameters in the
                    config.ini at the root of the project are present
                    and correct, and that the databse is running."""


# DECORATORS
def provide_db_connection(func):
    """
    Decorator which creates aq db connection object
    and passes it to the decorated function which
    uses it to connect with the db.

    After the decorated function is complete, the connection is closed.
    """

    @functools.wraps(func)
    def wrapper_provide_db_connection(*args, **kwargs):
        connection = get_db_connection()
        function_return = func(*args, **kwargs, connection=connection)
        connection.close()
        return function_return

    return wrapper_provide_db_connection


# FUNCTIONS
def get_db_connection_string() -> str:
    """
    Builds a database connection string using the configuration
    parameters in config.txt.
    """
    try:
        config_file_pth = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config.ini"
        )
        config = configparser.ConfigParser()
        config.read(config_file_pth)

        driver = config["DB_CONNECTION"]["obdc_driver"]
        server = config["DB_CONNECTION"]["db_server"]
        db_name = config["DB_CONNECTION"]["db_name"]
        db_user = config["DB_CONNECTION"]["db_user"]
        db_user_password = config["DB_CONNECTION"]["db_user_password"]

        connection_string = f"DRIVER={{{driver}}}; Server={server};Database={db_name};User Id={db_user};Password={db_user_password};Trusted_Connection=yes"
        return connection_string
    except Exception as e:
        print(
            "Could not generate connection string. Please check that the config.ini file is present in the project root folder"
        )


def get_db_connection():
    # Get db connection object
    sql_conn_str = get_db_connection_string()
    try:
        sql_conn = pyodbc.connect(sql_conn_str)
    except Exception as e:
        raise DBConnectionFailed
    return sql_conn
