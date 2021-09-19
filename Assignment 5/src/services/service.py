"""
    Service class for the list of complex numbers. This module manages all functionalities that the
    program must have.
"""

import copy
import random

from src.domain.entity import ComplexNumber
from src.domain.validators import AddComplexNumValidator, FilteringValidator


class ListService:
    """
    Class for the list service.
    This class manages multiple complex numbers into a list.

    :param add_validator: Validator for the adding process; instance of the AddComplexNumValidator class
    :param filter_validator: Validator for the filtering process; instance of the FilteringValidator class
    """

    def __init__(self, add_validator, filter_validator):
        if not isinstance(add_validator, AddComplexNumValidator):
            raise KeyError("The adding validator should be an AddComplexNumValidator instance!")
        if not isinstance(filter_validator, FilteringValidator):
            raise KeyError("The filter validator should be an FilteringValidator instance!")

        self.__entities = []
        self.__add_validator = add_validator
        self.__filter_validator = filter_validator
        self.__history = []

    def __len__(self):
        """
        The __len__ built-in method is overwritten so that the 'len()' function returns the numbers of complex
        numbers from the list when called on an instance of the ListService class.

        :return: How many numbers the list of numbers currently has.
        """
        return len(self.__entities)

    def __str__(self):
        """
        The __str__ built-in method is overwritten so that when an instance of the ListService class is
        printed, a list of instances of complex numbers is printed and not an object address.

        :return: String representation of the list of complex numbers
        """
        return str(self.__entities)

    def __contains__(self, item):
        """
        The __contains__ built-in method is overwritten so that it can be directly checked whether or not a
        complex number is present in the list, without the need for a separate function

        :param item: The complex number to check for in the list service
        :return: True if the complex number <item> is in the list; False otherwise
        """
        return item in self.__entities

    def __iter__(self):
        """
        The __iter__ built-in method is overwritten so that instances of the ListService class are iterable.
        This allows looping through the list of complex numbers.

        :return: Generator containing the list of complex numbers
        """
        return (num for num in self.__entities)

    def add_number(self, real=0, imag=0):
        """
        Method used for the adding process. Accepts a real and integer part, creates the new complex number to be
        added to the list, validates it, and if the validation process is successful the new complex number
        will be added to the list. Also, if the adding process is successful, a copy of the previous state
        of the list will be saved.

        :param real: The real part of the new complex number; integer
        :param imag: The imaginary part of the new complex number; integer
        :return: Returns the new complex number, in case it is needed
        :raise ComplexNumException: if the complex number is already in the list
        """
        new_number = ComplexNumber(real, imag)
        self.__add_validator.validate(self, new_number, )

        old_list = copy.deepcopy(self.__entities)
        self.__history.append(old_list)

        self.__entities.append(new_number)
        return new_number

    def find_num(self, complex_num):
        """
        Checks to see if the <complex_num> complex number is already in the list of complex numbers.

        :param complex_num: The complex number to check for
        :return: The position of complex number if it is already in the list; None otherwise
        """
        return next((index for index, num in enumerate(self) if complex_num == num), None)

    @staticmethod
    def generate_random_nums(n=10, real_lb=-100, real_ub=100, imag_lb=-100, imag_ub=100):
        """
        Method used for generating <n> random complex number.

        :param n: How many complex numbers to generate; integer
        :param real_lb: The lower bound of the real part of the complex numbers to be generated
        :param real_ub: The upper bound of the real part of the complex numbers to be generated
        :param imag_lb: The lower bound of the imaginary part of the complex numbers to be generated
        :param imag_ub: The upper bound of the imaginary part of the complex numbers to be generated
        :return: List of tuples, containing elements in the format (<real_part>, <imaginary_part>)
        """
        random_real_parts = random.sample(range(real_lb, real_ub + 1), n)
        random_imag_parts = random.sample(range(imag_lb, imag_ub + 1), n)
        return zip(random_real_parts, random_imag_parts)

    def fill_list(self, n=10, real_lb=-100, real_ub=100, imag_lb=-100, imag_ub=100):
        """
        Method used for filling the list of complex numbers with <n> complex numbers. Uses method
        generate_random_nums() for the random complex number generation.

        :param n: How many complex numbers to generate; integer
        :param real_lb: The lower bound of the real part of the complex numbers to be generated
        :param real_ub: The upper bound of the real part of the complex numbers to be generated
        :param imag_lb: The lower bound of the imaginary part of the complex numbers to be generated
        :param imag_ub: The upper bound of the imaginary part of the complex numbers to be generated
        """
        nums = self.generate_random_nums(n, real_lb, real_ub, imag_lb, imag_ub)
        for real, imag in nums:
            self.__entities.append(ComplexNumber(real, imag))

    def filter(self, start=None, end=None):
        """
        Method used for the filtering process. This method accepts two indices <start> and <end>, runs them through
        the filtering validator, and if the validator is successful the list of complex numbers is sliced such
        that it will only contain the numbers between the indices <start> and <end> (including the numbers
        at the indices <start> and <end>). Also, if successful, a copy of the list is saved in history states.

        :param start: The starting index of the filter
        :param end: The ending index of the filter
        :raise FilteringException: If the indices are not valid
        """

        start, end = self.__filter_validator.validate(self, start, end)

        old_list = copy.deepcopy(self.__entities)
        self.__history.append(old_list)

        keep_indices = slice(start, end)
        self.__entities = self.__entities[keep_indices]

    def undo(self):
        """
        Method for the undo process. 'Reverses' the last operation that modified the state of the data in the
        list.

        :raise: ValueError if the list is at the initial state, so undo is not possible anymore.
        """

        if len(self.__history) == 0:
            raise ValueError("Cannot undo anymore.\n"
                             "The list of numbers has the initial state.")

        self.__entities = self.__history.pop()
