# Standard Library Imports
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add project root to sys.path
sys.path.insert(0, PROJECT_ROOT)

# Local Imports
import DSTI_db_interface.cli_user_interface as cli

# 3rd party packages
app = cli.UserCLI()

if __name__ == "__main__":

    try:
        app.run_cli_app()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occured. Sorry about it.\n")
        print(f"Please report error:\n{e}\n...to your data engineer.")

