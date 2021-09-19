"""
    This module is responsible for everything UI-related. All inputs and prints are here.

    Calls between program modules
    ui -> service -> entity
    ui -> entity
"""

from src.domain.validators import FilteringException, ComplexNumException, InputValidator
from src.services.service import ListService


class Console:
    """
    Class for the console.
    We will use instances of this class to run the program.

    :param service: The list service needed for the list of complex numbers ('dependency injection'); instance
    of the ListService class
    :param input_validator: Validator for the input string given by the user into the console; instance of
    the InputValidator class
    """

    def __init__(self, service, input_validator):
        if not isinstance(service, ListService):
            raise TypeError("The service should be a ListService instance!")
        if not isinstance(input_validator, InputValidator):
            raise TypeError("The input validator should be an InputValidator instance!")

        self.__list_service = service
        self.__input_validator = input_validator

    @staticmethod
    def ui_print_menu():
        print("The following commands are currently available:\n"
              "\t1 - Input a new complex number into the console and add it to the list\n"
              "\t2 - Display on the screen the current list of numbers\n"
              "\t3 - Filter the list so that it contains only the numbers between the console given indices "
              "<start> and <finish>\n"
              "\t4 - Undo the last operation\n"
              "\tx - Exit")

    def ui_add_number(self):
        """
        Method that starts the 'adding to list' process. This method accepts a valid input complex number,
        validates the input string (checks to see if the given string is in an accepted format), and then calls
        the adding method of the service. If successful, a message will be displayed on the screen.
        """
        num_str = input("Please give a complex number in the format 'a+bi': ")
        real_part, imag_part = self.__input_validator.validate(num_str)
        number_added = self.__list_service.add_number(real_part, imag_part)
        print(f"\nThe given complex number {number_added} has been added to the list of numbers.")

    def ui_print_all(self):
        """
        Method for displaying on the console the current list of numbers from the service list.
        """
        print("This is the current list of numbers: ")
        for index, num in enumerate(self.__list_service):
            print(f"\t{index+1})", num)

    def ui_filter(self):
        """
        Method that starts the filtering process. This method accepts two valid indices, and then calls the
        filtering method of the list service.
        """
        print(f"Note: Indices should be between {1} and {len(self.__list_service)}.")
        start = input("Please give us the starting index of the filter: ")
        end = input("Please give us the ending index of the filter: ")
        print()

        try:
            start = int(start)
            end = int(end)
        except ValueError:
            raise ValueError("The indices should be non-negative integers.")

        self.__list_service.filter(start, end)
        print("The filter process has been successful.")

    def ui_undo(self):
        """
        Method that starts the undo process. This method simply calls the undo method of the list service.
        """
        self.__list_service.undo()
        print("The last command that modified the list has been reversed.")

    def ui_init_list(self, n=10, real_lb=-100, real_ub=100, imag_lb=-100, imag_ub=100):
        """
        Method that initialises the list of numbers with  'n' random complex numbers.
        The parameter n, as well as the lower and upper bound of the generated real and imaginary parts of
        the complex numbers can be changed. This method simply calls the filling method of the list service.
        """
        self.__list_service.fill_list(n, real_lb, real_ub, imag_lb, imag_ub)
        print(f"The list has been initialized with {n} random complex numbers.")

    def run_console(self):
        """
        Runs the console.
        """
        commands = {'1': self.ui_add_number, '2': self.ui_print_all,
                    '3': self.ui_filter, '4': self.ui_undo}
        self.ui_init_list()

        while True:
            try:
                self.ui_print_menu()
                cmd = input("Give a valid command: ")
                print()

                if cmd in commands.keys():
                    commands[cmd]()
                elif cmd == 'x':
                    break
                else:
                    raise KeyError("Invalid command.")

            # Need to handle KeyError separately, so that we don't print the quotes of KeyError
            except KeyError as ke:
                print(str(ke)[1:-1])

            except (ValueError, FilteringException, ComplexNumException, TypeError) as err:
                print(str(err))

            print()
