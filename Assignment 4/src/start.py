"""
This module assembles the program and starts the user interface.
It ties everything together.
"""

import traceback

from src.tests.tests import run_all_tests
from src.ui.console import run_menu_cmd

if __name__ == "__main__":
    run_all_tests()

    print("Hello!")

    try:
        run_menu_cmd()

    except Exception as ex:
        print("Unknown error caught: ", ex)
        traceback.print_exc()

    print("Have a great day!")
