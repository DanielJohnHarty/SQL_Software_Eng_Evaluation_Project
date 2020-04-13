# Quickstart

Import or sun as script

get_all_survey_data(update_view=True) -> Returns the latest AllSurveyData. If update_view is True, calls update_vw_AllSurveyData_if_obsolete with latest data

run_sql_select_query(your_select_query_string)

update_vw_AllSurveyData_if_obsolete(live_survey_data=None) -> If live_survey_data is None, the latest will be queried from the db using get_all_survey_data


# Project Scope

To create an application written in Python3 to facilitate data consumers to a specific 'always-fresh' view on live production data. Project restrictions apply.

### Project Restrictions

- Only use SELECT queries on DB tables
- Only create or alter views
- Provide an always fresh alternative using Python3 without using SQL functions or triggers on the database server

### Project Implementation Requirements

1. Gracefully handle the connection to the database server.
2. Replicate the algorithm of the dbo.fn_GetAllSurveyDataSQL stored function.
3. Replicate the algorithm of the trigger dbo.trg_refreshSurveyView for
creating/altering the view vw_AllSurveyData whenever applicable.
4. For achieving (3) above, a persistence component (in any format you like: CSV, XML,
JSON, etc.), storing the last known surveys’ structures should be in place. It is not
acceptable to just recreate the view every time: the trigger behaviour must be
replicated.
5. Of course, extract the “always-fresh” pivoted survey data, in a CSV file, adequately
named.


## Development Environment

- Python Version: 3.8.2
- Testing Framework: pytest-5.4.1
- Development OS: Windows 10
- IDE: Visual Studio Code
- Anaconda Distribution (conda 4.8.2)

### Recreating Development Envirnoment Using Conda

This project was developed using Anaconda (conda 4.8.2). To recreate the development environment use the command:
 
     **conda env create -f conda_env.yml**

Note that the *conda_env.yml* is at the project root and includes a full description of the environment used during development and will recreate it as accurately as possible.

# Installing dependencies in current python environment

**Necessary dependencies are installed automatically into current the python installation** on execution of *__init__.py* (running as a script) or on *importing as a module*.

**This process requires the requirements.txt file at the project root and that pip is installed in the current python environment**.

# Configuration details

- The purpose of the app/python package requires connecting to a database. The parameters required to connect to the database **must be present and correct in a file called config.ini at the project root**. This is the only configuration you need to do as a user, and you only need to do it once.

-  **Access to the contents of this file must be restricted**.

- The details of which configuration parameters are necessary are in the config_defailt.ini file. **The config_default.ini file should be used as a template for your config.ini file**.


# Running Tests

At the project root, ensure you have **pytest** installed and run the command:

```
pytest -v -s
```

