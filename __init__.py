# Standard Library Imports
import os
import subprocess
import sys


# Add project root to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Local Imports
import DSTI_db_interface.dependency_installation as dependency_installation
import DSTI_db_interface.db_api as db_api
import DSTI_db_interface.db_connection as db_connection
import DSTI_db_interface.queries_and_dynamic_queries as queries_and_dynamic_queries

# Install any missing dependencies for import
dependency_installation.install_dependencies()


PROJECT_NAME = "DSTI_db_interface"

if __name__ == "__main__":

    try:
        # Run as command line app
        app_file_pth = os.path.join(
            os.path.dirname(__file__), PROJECT_NAME, "Scripts", "app.py"
        )
        subprocess.check_call([sys.executable, app_file_pth])
    except KeyboardInterrupt:
        pass
