# Standard Library Imports
import os
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Add project root to sys.path
sys.path.insert(0, PROJECT_ROOT)

# Local Imports
# Import part of test
# import DSTI_db_interface.dependency_installation as di


def test_install_dependencies_as_import():
    """
    Test that when module is imported, dependency
    installation deosn't raise an exception
    """
    # Local Imports
    import DSTI_db_interface.dependency_installation as di


def test_install_dependencies_as_script():
    """
    Test that when module is imported, dependency
    installation deosn't raise an exception
    """
    run_as_script_pth = os.path.join(PROJECT_ROOT, "__init__.py")

    subprocess.check_call([sys.executable, run_as_script_pth])


def test_requirements_txt_at_project_root():
    """
    Test returns false if requirements.txt is not
    present in the project root
    """
    requirements_ok = os.path.exists(os.path.join(PROJECT_ROOT, "requirements.txt"))

    assert requirements_ok is True

def test_project_root_in_path():
    """
    Ensure that the project root has been correctly added
    to the Python import path sys.path
    """
    assert PROJECT_ROOT in sys.path