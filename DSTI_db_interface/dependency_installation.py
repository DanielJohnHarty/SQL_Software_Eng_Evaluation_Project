# Standard library imports
import os
import subprocess
import sys


def install_dependencies() -> None:
    """
    Use the local environment Python executables pip
    to install all dependencies in the requirement.txt file.
    """
    try:
        requirements_txt_pth = os.path.join(
            # By convention, requirements.txt is at project root
            os.path.dirname(os.path.dirname(__file__)),
            "requirements.txt",
        )
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", requirements_txt_pth]
        )
        print("Dependencies ok!")

    except Exception as e:
        print(
            "    -> This could lead to missing dependencies"
            + ",unexpected behaviour and program failure."
        )
