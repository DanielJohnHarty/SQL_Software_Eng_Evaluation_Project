- Python Version: 3.8.2
- Testing Framework: pytest-5.4.1
- Development OS: Windows 10
- IDE: Visual Studio Code
- Anaconda Distribution (conda 4.8.2)

# Recreating dev environment
### Conda

This project was developed using Anaconda (conda 4.8.2). To recreate the development environment use the command:
 
     **conda env create -f conda_env.yml**

Note that the *conda_env.yml* is at the project root and includes a full description of the environment used during development and will recreate it as accurately as possible.

# Installing dependencies in current python environment

Necessary dependencies are installed automatically **into current the python installation** on execution of update_view.py. **This process requires the requirements.txt file at the project root and that pip is installed in the current python environment**.


# Configuration details
- Add the necessary configuration details in to config.ini. **Access to the contents of this file must be restricted**.

- The details of which configuration parameters are necessary are in the config_defailt.ini file. **The config_default.ini file should be used as a template for your config.ini file**.


___

# Project Restrictions

- Only use SELECT queries on DB tables
- Only create or alter views
- Provide an always fresh alternative using Python3 without using SQL functions or triggers on teh database server

# Project Implementation Requirements

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


# Running Tests

At the project root, ensure you have **pytest** installed and run the command:

```
pytest -v -s
```

