






# Standard library imports
import os
import subprocess
import sys
import configparser


# External library imports
import pandas as pd
import pyodbc


def get_db_connection_string()-> str:
    """
    Builds a database connection string using the configuration
    parameters in config.txt.
    """
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        driver = config['DB_CONNECTION']['obdc_driver']
        server = config['DB_CONNECTION']['db_server']
        db_name = config['DB_CONNECTION']['db_name']
        db_user = config['DB_CONNECTION']['db_user']
        db_user_password = config['DB_CONNECTION']['db_user_password']

        connection_string = f'DRIVER={{{driver}}}; Server={server};Database={db_name};User Id={db_user};Password={db_user_password};Trusted_Connection=yes'
        return connection_string
    except Exception as e:
        print("Could not generate connection string. Please check that the config.ini file is present in the project root folder")


def install_dependencies(requirements_txt_path='requirements.txt')-> None:
    """
    Use the local environment Python executables pip
    to install all dependencies in the requirement.txt file.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies ok!")

    except Exception as e:
        print("    -> This could lead to missing dependencies" + 
              ",unexpected behaviour and program failure.")


if __name__ == '__main__':

    # Install any missing dependencies
    install_dependencies()

    # Get db connection object
    sql_conn_str = get_db_connection_string()
    sql_conn = pyodbc.connect(sql_conn_str)
    
    # Test connection
    query = "SELECT * FROM [Survey_Sample_A19].[dbo].[vw_AllSurveyData] ORDER BY SurveyId, UserId"
    df = pd.read_sql(query, sql_conn)
    print(df.head(3))

