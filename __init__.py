#Standard Library Imports
import os
import subprocess
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Local Imports
import DSTI_db_interface.dependency_installation as di

# Install any missing dependencies
di.install_dependencies()


PROJECT_NAME = 'DSTI_db_interface'

if __name__ == '__main__':

    # Run main.py
    main_file_pth = os.path.join(os.path.dirname(__file__), PROJECT_NAME,'main.py')

    subprocess.check_call([sys.executable,  main_file_pth])
