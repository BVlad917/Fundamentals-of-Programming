"""
    Module responsible for all of the program's validators
"""

import re


class ListException(Exception):
    """
    Custom exception class for the list service. Inherits from the base exception, and all exceptions related
    to the service in one way or another will inherit from this exception.
    """
    pass


class ComplexNumException(ListException):
    """
    Custom exception class for the complex number 'adding to list' process. This exception is used in the case
    that the complex number to be added to the list is already in the list.
    """
    pass


class FilteringException(ListException):
    """
    Custom exception class for the filtering process. This exception is used in the case that the filtering
    indices given by the user are invalid.
    """
    pass


class AddComplexNumValidator:
    """
    Validator for the 'adding to list' process. Checks to see if the complex number to be added is already in
    the list. If it is, a ComplexNumException is raised.
    """

    @staticmethod
    def validate(list_service, complex_num):
        index = list_service.find_num(complex_num)
        if index is not None:
            raise ComplexNumException(f"Cannot add.\n"
                                      f"The number {complex_num} is already in the list at position {index + 1}.")


class FilteringValidator:
    """
    Validator for the filtering process. Checks to see if the given filtering indices are invalid or not.
    The filtering indices are invalid if they are both less than 1 or both greater than the length of the list.
    If the filtering indices can be interpreted as correct (e.g., they are given in the reverse order, one (and only
    one) index is outside of the range, etc), the program will correct them and perform the filtering.
    """

    @staticmethod
    def validate(list_service, start, end):

        start = 1 if start is None else start
        end = len(list_service) if end is None else end

        if (start > len(list_service) and end > len(list_service)) or \
                (start <= 0 and end <= 0):
            raise FilteringException(f"Cannot filter.\n"
                                     f"Filter indices must be between {1} and {len(list_service)}.")

        if start > end:
            start, end = end, start

        start = start - 1

        start = max(start, 0)
        end = min(end, len(list_service))

        return start, end


class InputValidator:
    """
    Validator for the complex number given by the user as input. Removes white spaces, checks to see if the user
    sent gibberish (in which case a ValueError is raised), and if everything seems right, the string will be
    parsed by the program into a tuple in the format (<real_part>, <imaginary_part>)
    """

    @staticmethod
    def validate(input_str):
        input_str = input_str.replace(' ', '')

        if '-i' in input_str:
            input_str = input_str.replace('-i', '-1i')
        if '+i' in input_str:
            input_str = input_str.replace('+i', '+1i')
        if input_str == 'i':  # Edge case we need to take care of
            input_str = '+1i'

        if len(re.findall(r"[^0-9i+-]", input_str)) > 0:
            raise ValueError("Error! Please enter a valid complex number in the format 'a+bi'.")

        nums_str = re.findall(r"-?\d+i?", input_str)

        if len(nums_str) == 1:

            if 'i' in nums_str[0]:
                try:
                    return 0, int(nums_str[0].replace('i', ''))
                except ValueError:
                    raise ValueError("Error! The real and imaginary parts should be integers.")

            else:
                try:
                    return int(nums_str[0]), 0
                except ValueError:
                    raise ValueError("Error! The real and imaginary parts should be integers.")

        elif len(nums_str) == 2:
            if 'i' not in nums_str[0] and 'i' not in nums_str[1]:
                raise ValueError("Error! We cannot support multiple real parts.")

            elif 'i' in nums_str[1] and 'i' not in nums_str[0]:
                try:
                    return int(nums_str[0]), int(nums_str[1].replace('i', ''))
                except ValueError:
                    raise ValueError("Error! The real and imaginary parts should be integers.")

            elif 'i' in nums_str[0] and 'i' not in nums_str[1]:
                try:
                    return int(nums_str[1]), int(nums_str[0].replace('i', ''))
                except ValueError:
                    raise ValueError("Error! The real and imaginary parts should be integers.")

            else:  # If we reach this, there are i's in both terms => Invalid
                raise ValueError("Error! We cannot support multiple imaginary parts.")

        else:
            raise ValueError("Error! Please provide at most 2 numbers: the integer part and the imaginary part.")
