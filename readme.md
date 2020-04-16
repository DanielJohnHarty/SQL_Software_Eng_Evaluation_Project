# Quickstart



## Run as a CLI

From the project route, enter the command:
```
python DSTI_db_interface\Scripts\app.py
```

or alternatively:

```
python __init__.py
```

Then follow the onscreen prompts.

***This is the simplest way for people less comfortable with Python to interact with the DSTI database.***



## Import as Python module:


The ***DSTI_db_interface*** folder contains Python modules which can be imported into your Python interpreter.

The available modules are:

1. ***db_api***
2. cli_user_interface
3. db_connection
4. file_utilities_queries_and_dynamic_queries


db_api in the above list is highlighted because it is the only module you will need to import.

To import it, **from the project root directory**, enter your Python interpreter enter the following command:

```
import DSTI_db_interface.db_api as db
```

Now you can download the most recent AllSurveyDatas from the database tables:

```
all_survey_data_as_dataframe = db.get_all_survey_data()
```

This grabs the latest up to date data ***and updates the view vw_AllSurveyData**. If you do not want ot update the view vw_AllSurveyData, use the update_view=False parameter like so:

```
all_survey_data_as_dataframe = db.get_all_survey_data(update_view=False)
```

You can also update the view vw_AllSurveyData without returning the data as a dataframe:
```
db.update_vw_AllSurveyData_if_obsolete()
```

> If you see messages about checkpoint hashes you might ask yourself what they are and if you need to pay attention to them.
> If you're asking yourself this question then you probably don't need to. If you're interested though,
> a checkpoint is a small text string representing a dataset. A new checkpoint hash means data has changed and 
> the new hash represents the latest 'checkpoint'.


If you want to go yolo and run your own SELECT query, you can do so as follows:
```
my_qry = 'SELECT * FROM MyTable;'
resultset_as_dataframe = db.run_sql_select_query(my_qry)
```

### Note: Only SELECT queries are permitted. You can create and modify views.
### Note: You **don't** need to deal with database connections. A new one is created and closed  each time you run a query.



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

