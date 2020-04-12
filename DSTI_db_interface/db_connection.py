# Standard library imports
import configparser
import functools
import os

# Local Imports

# External library imports
import pyodbc


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


def get_db_connection_string() -> str:
    """
    Builds a database connection string using the configuration
    parameters in config.txt.
    """
    try:
        config_file_pth = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")
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
        raise Exception(
            f'Error "{e}" connecting to database. Check your connection parameters in config.ini and try again.'
        )

    return sql_conn

