import random
import re

from domain.person import Person
from domain.validators import PersonIDException, PersonNameException, PersonPhoneNumberException, UndoRedoException
from utils.filter import Filter


class PersonService:
    """
    Class used to represent the person service
    Manages all person-related functionalities
    :param person_repository: repository entity used as repository for the persons
    :param person_ids_validator: PersonIDValidator validator that checks (and parses) the user-given person IDs
    :param phone_number_validator: PhoneNumberValidator validator that checks (and parses) the user-given phone numbers
    """

    def __init__(self, person_repository, person_ids_validator, phone_number_validator,
                 undo_repository, redo_repository):
        self.__person_repository = person_repository
        self.__person_ids_validator = person_ids_validator
        self.__phone_number_validator = phone_number_validator
        self.__undo_repository = undo_repository
        self.__redo_repository = redo_repository
        self.__filter = Filter().filter

    def get_inverse_operation_and_args(self, fn, *args):
        """
        Returns the logical inverse of a given function and the arguments that this logical inverse
        will need in order to be run.
        :param fn: The function whose logical inverse the program will return; type function object
        :param args: The arguments given by the caller function; only the necessary arguments for the
        logical inverse function will be saved on the stack
        :return: The logical inverse function and its arguments
        :raise UndoRedoException: If a non-invertible or a not-supported function is passed; This is a
        programming error; it should never happen
        """
        inverse_fn_and_args = {self.add_person: (self.delete_person_by_id, args[:1]),
                               self.delete_person_by_id: (self.add_person, args),
                               self.update_person_name: (self.update_person_name, args),
                               self.update_person_phone_number: (self.update_person_phone_number, args)}
        if fn in inverse_fn_and_args.keys():
            return inverse_fn_and_args[fn]
        else:  # Programming error
            raise UndoRedoException("Error! Non-invertible operation.\nInverse function could not be registered.")

    def save_undo_operation(self, fn, *args):
        """
        Saves the logical inverse of an operation on the undo stack
        :param fn: The function whose logical inverse function we want saved on the undo stack
        :param args: The arguments of the caller function out of which the logical inverse will choose
        just the necessary arguments
        """
        inverse_op, args = self.get_inverse_operation_and_args(fn, *args)
        self.__undo_repository.record_inverse_operations(inverse_op, *args)

    def save_redo_operation(self, fn, *args):
        """
        Saves the logical inverse of an operation on the redo stack
        :param fn: The function whose logical inverse function we want saved on the redo stack
        :param args: The arguments of the caller function out of which the logical inverse will choose
        just the necessary arguments
        """
        inverse_op, args = self.get_inverse_operation_and_args(fn, *args)
        self.__redo_repository.record_inverse_operations(inverse_op, *args)

    def add_person(self, person_id, name, phone_number, record_undo=True, record_redo=False, as_redo=False):
        """
        Adds a new person to the person repository
        :param person_id: The ID of the person to be added; string/integer
        :param name: The name of the person to be added; string
        :param phone_number: The phone number of the person to be added; string
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool

        :return: the newly added person

        :raise PersonIDException: if the given person ID is not an integer, is not positive, or is already in the
        person repository.
        :raise PersonNameException: If the given name is not a string or is already registered
        :raise PersonPhoneNumberException: If the given phone number is not a string or is already registered
        """
        if not isinstance(name, str):
            raise PersonNameException(f"Error! Invalid input person name: {name}")
        if not isinstance(phone_number, str):
            raise PersonPhoneNumberException(f"Error! Invalid input phone number: {phone_number}")

        phone_number = self.__phone_number_validator.validate(phone_number)
        name = name.strip().title()
        name = ' '.join(name.split())

        # This is a programming error. If the input parsing is correct the below
        # exceptions should never be raised
        try:
            person_id = int(person_id)
        except ValueError:
            raise PersonIDException("Error! The person ID must be a positive integer!")

        if person_id <= 0:
            raise PersonIDException("Error! The person ID must be a positive integer!")
        if person_id in self.__person_repository.get_all_ids():
            raise PersonIDException(f"The ID '{person_id}' is already registered.")
        if name in self.get_all_names():
            raise PersonNameException(f"The name '{name}' is already registered.")
        if phone_number in self.get_all_phone_numbers():
            raise PersonPhoneNumberException(f"The phone number '{phone_number}' is already registered.")

        new_person = Person(person_id, name, phone_number)
        self.__person_repository.add_to_repo(new_person)

        if record_undo:
            self.save_undo_operation(self.add_person, new_person.id, new_person.name, new_person.phone_number)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.add_person, new_person.id, new_person.name, new_person.phone_number)

        return new_person

    def delete_person_by_id(self, person_id, record_undo=True, record_redo=False, as_redo=False):
        """
        Deletes a person from the person repository.
        :param person_id: The ID of the person to be deleted; string/integer
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool
        :return: The person that was just removed; <Person> class instance
        :raise PersonIDException: if the given person ID is not a string, is not positive, or is not in the database
        """
        try:
            person_id = int(person_id)
        except ValueError:
            raise PersonIDException("Error! The person ID must be an integer.")
        if person_id <= 0:
            raise PersonIDException("Error! The person ID must be a positive integer.")
        person_to_remove, _ = self.find_person_by_id(person_id)
        if person_to_remove is None:
            raise PersonIDException(f"Error! There is no person with the ID {person_id} in the database.")
        self.__person_repository.delete_by_id(person_id)

        if record_undo:
            self.save_undo_operation(self.delete_person_by_id, person_to_remove.id, person_to_remove.name,
                                     person_to_remove.phone_number)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.delete_person_by_id, person_to_remove.id, person_to_remove.name,
                                     person_to_remove.phone_number)

        return person_to_remove

    def update_person_phone_number(self, person_id, person_new_phone_number, record_undo=True,
                                   record_redo=False, as_redo=False):
        """
        Updates a person's phone number
        :param record_redo:
        :param person_id: The ID of the person whose phone number needs to be changed; string/integer
        :param person_new_phone_number: The new phone number of the person; string
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool

        :return: The ID of the person whose number was changed (positive integer) and the new phone number (string)
        :raise PersonIDException: if the given person ID is not an integer, is not positive, or is not
        in the database
        :raise PersonPhoneNumberException: if the given phone number is already registered in the database.
        """
        new_phone_number = self.__phone_number_validator.validate(person_new_phone_number)
        try:
            person_id = int(person_id)
        except ValueError:
            raise PersonIDException("Error! The person ID has to be an integer!")
        if person_id <= 0:
            raise PersonIDException("Error! The person ID has to be a positive integer!")

        if new_phone_number in self.get_all_phone_numbers():
            raise PersonPhoneNumberException(f"Error! The phone number '{new_phone_number}' is already registered.")

        person, _ = self.find_person_by_id(person_id)
        if person is None:
            raise PersonIDException(f"Error! There is no person with ID '{person_id}' in the database.")

        old_phone_number = person.phone_number
        updated_person = Person(person.id, person.name, new_phone_number)
        self.__person_repository.update(updated_person)

        if record_undo:
            self.save_undo_operation(self.update_person_phone_number, person.id, old_phone_number)
            if not as_redo: self.__redo_repository.clear_stack()

        if record_redo:
            self.save_redo_operation(self.update_person_phone_number, person.id, old_phone_number)

        return person_id, new_phone_number, old_phone_number

    def update_person_name(self, person_id, person_new_name, record_undo=True, record_redo=False, as_redo=False):
        """
        Updates a person's name
        :param person_id: The ID of the person whose name needs to be updated; integer/string
        :param person_new_name: The new name of the person; string
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool

        :return: The ID of the person whose name was changed (positive integer) and the new name of the person (string)
        :raise PersonIDException: if the given person ID is not an integer, is not positive, or is not registered
        in the database
        :raise PersonNameException: if the given name is already registered in the person repository
        """
        try:
            person_id = int(person_id)
        except ValueError:
            raise PersonIDException("Error! The person ID has to be a positive integer!")
        if person_id <= 0:
            raise PersonIDException("Error! The person ID has to be a positive integer!")

        person_new_name = person_new_name.strip().title()
        if person_new_name in self.get_all_names():
            raise PersonNameException(f"Error! The name '{person_new_name}' is already registered in the database.")

        person, _ = self.find_person_by_id(person_id)
        if person is None:
            raise PersonIDException(f"Error! There is no person with ID '{person_id}' registered.")

        person_old_name = person.name
        updated_person = Person(person.id, person_new_name, person.phone_number)
        self.__person_repository.update(updated_person)

        if record_undo:
            self.save_undo_operation(self.update_person_name, person.id, person_old_name)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.update_person_name, person.id, person_old_name)

        return person_id, person_new_name, person_old_name

    def find_person_by_id(self, person_id):
        """
        Returns a person entity by ID
        """
        try:
            person_id = int(person_id)
        except ValueError:
            raise PersonIDException("Error! The person ID has to be a positive integer!")
        if person_id <= 0:
            raise PersonIDException("Error! The person ID has to be a positive integer!")

        return self.__person_repository.find_by_id(person_id)

    def get_name_of_person_by_id(self, person_id):
        """
        Returns the name of a person by ID
        """
        try:
            person_id = int(person_id)
        except ValueError:
            raise PersonIDException("Error! The person ID has to be a positive integer!")
        if person_id <= 0:
            raise PersonIDException("Error! The person ID has to be a positive integer!")

        found_person, _ = self.find_person_by_id(person_id)
        if found_person is None:
            raise PersonIDException(f"Error! There is no person with ID '{person_id}' registered.")
        return found_person.name

    def get_all_persons(self):
        """
        Returns all the currently registered persons from the repository
        """
        return self.__person_repository.elements

    def get_all_ids(self):
        """
        Returns all the person IDs currently registered in the person repository
        """
        return self.__person_repository.get_all_ids()

    def get_all_names(self):
        """
        Returns all the person names currently registered in the person repository
        """
        return [person.name for person in self.__person_repository.elements]

    def get_all_phone_numbers(self):
        """
        Returns all the phone numbers currently registered in the person repository
        """
        return [person.phone_number for person in self.__person_repository.elements]

    def search_by_name(self, name):
        """
        Returns all persons which (partially) match the given argument <name>.
        The search is case-insensitive and a type of partial string matching.
        :param name: The string the program will search for in the persons database
        :return: All persons whose name match the argument <name>; list of <Person> instances
        """
        return self.__filter(self.get_all_persons(), lambda x: name.lower().strip() in x.name.lower().strip())

    def search_by_phone_number(self, phone_number):
        """
        Returns the person with phone number <phone_number>. If no such person is found, returns None.
        :param phone_number: The phone number to search for in the persons database; string
        :return: <Person> instance representing the found person if there exists a registered person with
        phone number <phone_number>; None otherwise
        """
        if len(re.findall("[^0-9-+ ]+", phone_number)) or len([c for c in phone_number if c == '+']) > 1:
            raise PersonPhoneNumberException("Invalid phone number search input. Can only contain digits, hyphens,"
                                             "spaces, and a plus sign(+).")
        phone_number = phone_number.replace(' ', '')
        phone_number = phone_number.replace('-', '')
        phone_number = phone_number.replace('+4', '')
        return self.__filter(self.get_all_persons(), lambda x: phone_number in x.phone_number.replace(' ', ''))

    def fill_repo_with_random_persons(self, n=10, id_lb=1, id_ub=100):
        """
        Fills the repository with randomly generated persons
        :param n: How many random persons to fill the person repository with
        :param id_lb: The lower bound of the random IDs to be generated
        :param id_ub: The upper bound of the random IDs to be generated
        """
        random_ids, random_names, random_phone_numbers = self.generate_random_persons(n, id_lb, id_ub)
        for id_, name, phone_num in zip(random_ids, random_names, random_phone_numbers):
            self.add_person(id_, ' '.join(name), phone_num)

    def generate_random_persons(self, n=10, id_lb=1, id_ub=100):
        """
        Generates random persons
        :param n: How many random persons to generate
        :param id_lb: The lower bound of the random IDs to be generated
        :param id_ub: The upper bound of the random IDs to be generated
        :return random_ids: The randomly generated person IDs
        :return random_names: The randomly generated names
        :return random_phone_numbers: The randomly generated phone numbers
        """
        random_ids = self.generate_random_ids(n, id_lb, id_ub)
        random_names = self.generate_random_names(n)
        random_phone_numbers = self.generate_random_phone_numbers(n)
        return random_ids, random_names, random_phone_numbers

    def generate_random_ids(self, n=10, min_id=1, max_id=100):
        """
        Generated random person IDs
        :param n: How many random IDs to generate
        :param min_id: Lower bound for the generated IDs
        :param max_id: Upper bound for the generated IDs
        :return: List of randomly generated IDs
        """
        all_ids = self.__person_repository.get_all_ids()
        random_ids = random.sample(list(set(range(min_id, max_id)) - set(all_ids)), k=n)
        return random_ids

    @staticmethod
    def generate_random_names(n=10):
        """
        Generates Random names, by reading them randomly from a file
        :param n: How many names to generate
        :return random_first_names: The randomly generated first names
        :return random_last_names: The randomly generated last names
        """
        first_names_list_file = 'first_names_list.txt'
        last_names_list_file = 'last_names_list.txt'

        with open(r'C:/Users/VladB/Documents/GitHub/a678-BVlad917/' + first_names_list_file, 'r') as file:
            first_names = file.readlines()
            random_first_names = random.sample(first_names, n)
            random_first_names = [random_first_name.title().strip() for random_first_name in random_first_names]

        with open(r'C:/Users/VladB/Documents/GitHub/a678-BVlad917/' + last_names_list_file, 'r') as file:
            last_names = file.readlines()
            random_last_names = random.sample(last_names, n)
            random_last_names = [random_last_name.title().strip() for random_last_name in random_last_names]

        return zip(random_first_names, random_last_names)

    @staticmethod
    def generate_random_phone_numbers(n=10):
        """
        Generates random phone numbers in the romanian format.
        :param n: How many random phone numbers to generate
        :return: The list of randomly generated phone numbers
        """
        random_phone_nums = []
        phone_num_first_digit = '0'
        phone_num_second_digit = ['2', '7']
        phone_num_third_digit = ['2', '3', '4', '5']
        phone_num_last_seven_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        for _ in range(n):
            random_num = phone_num_first_digit + \
                         random.choice(phone_num_second_digit) \
                         + random.choice(phone_num_third_digit)
            last_digits = random.choices(phone_num_last_seven_digits, k=7)
            random_num = random_num + ''.join(last_digits)
            random_phone_nums.append(random_num)

        return random_phone_nums

    # --------------------------------- #
    # ---------- GUI helpers ---------- #
    # --------------------------------- #

    def get_all_persons_string(self):
        s = ""
        all_persons = self.get_all_persons()
        if len(all_persons) == 0:
            return "There are no persons currently registered in the database.\n"
        for index, person in enumerate(all_persons):
            s = s + f"{index + 1}) {person}"
        return s

    def get_search_person_by_name_string(self, search_name):
        found_persons = self.search_by_name(search_name)
        if len(found_persons) == 0:
            return f"There are no persons in the database containing the name '{search_name.strip()}'.\n"
        s = f"These are all the persons whose name contain '{search_name.strip()}':\n"
        for index, person in enumerate(found_persons):
            s = s + f"{index + 1}) {person}"
        return s

    def get_search_persons_by_phone_number_string(self, search_phone_number):
        found_persons = self.search_by_phone_number(search_phone_number)
        if len(found_persons) == 0:
            return f"There are no persons whose phone numbers contain '{search_phone_number.strip()}'.\n"
        s = f"These are all the persons whose phone number contain '{search_phone_number.strip()}':\n"
        for index, person in enumerate(found_persons):
            s = s + f"{index + 1}) {person}"
        return s
