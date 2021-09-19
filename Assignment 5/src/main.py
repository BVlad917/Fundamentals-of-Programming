"""
    The main module of our program. This module's purpose is to tie everything together.
"""

import traceback

from src.domain.validators import InputValidator, FilteringValidator, AddComplexNumValidator
from src.services.service import ListService
from src.tests.tests import test_all
from src.ui.console import Console


if __name__ == "__main__":

    print("Hello!")

    try:
        add_validator = AddComplexNumValidator()
        filter_validator = FilteringValidator()
        input_validator = InputValidator()

        service = ListService(add_validator, filter_validator)
        test_all()

        console = Console(service, input_validator)
        console.run_console()

    except Exception as ex:
        print("Unknown exception caught!", ex)
        traceback.print_exc()

    print("Have a great day!")
