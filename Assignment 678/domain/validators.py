import datetime
import re


# ------------------------------------------- #
# ------------ CUSTOM EXCEPTIONS ------------ #
# ------------------------------------------- #

class PersonException(Exception):
    def __init__(self, message):
        super().__init__(message)


class PersonIDException(PersonException):
    def __init__(self, message):
        super().__init__(message)


class PersonPhoneNumberException(PersonException):
    def __init__(self, message):
        super().__init__(message)


class PersonNameException(PersonException):
    def __init__(self, message):
        super().__init__(message)


class ActivityException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ActivityIDException(ActivityException):
    def __init__(self, message):
        super().__init__(message)


class ActivityDateException(ActivityException):
    def __init__(self, message):
        super().__init__(message)


class ActivityTimeException(ActivityException):
    def __init__(self, message):
        super().__init__(message)


class ActivityPersonException(ActivityException):
    def __init__(self, message):
        super().__init__(message)


class ConsoleException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ConsoleCommandException(ConsoleException):
    def __init__(self, message):
        super().__init__(message)


class UndoRedoException(Exception):
    def __init__(self, message):
        super().__init__(message)


class UndoException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RedoException(Exception):
    def __init__(self, message):
        super().__init__(message)


# ---------------------------------------------- #
# ----------------- VALIDATORS ----------------- #
# ---------------------------------------------- #


# ---------------- PERSON VALIDATORS ---------------- #


class PhoneNumberValidator:
    """
    Validator for the phone number input (coming from the user).
    """

    @staticmethod
    def validate(phone_number_str):
        """
        Checks to see if the input was given in the accepted format and if it was it parses this given string
        into the phone number string that the program will work with.
        :param phone_number_str: The phone number given by the user; string
        :return: The phone number in the format that the program will work with
        :raise PersonPhoneNumberException: If invalid characters were given in the phone number
        :raise PersonPhoneNumberException; If the given phone number doesn't have 10 digits, if the given phone
        number doesn't start with a 0, if the given phone number doesn't have an accepted digit as the
        second or third digits (accepted in the romanian format)
        """
        valid_first_digits = ['0']
        valid_second_digits = ['2', '7']
        valid_third_digits = ['2', '3', '4', '5', '6']

        non_phone_number_characters = re.findall("[^0-9() +-]+", phone_number_str)
        if len(non_phone_number_characters):
            raise PersonPhoneNumberException("Error! Phone numbers should contain digits, spaces and hyphens only!")

        phone_number_str = phone_number_str.replace(' ', '')
        phone_number_str = phone_number_str.replace('+4', '')
        phone_number_str = phone_number_str.replace('-', '')
        if len(phone_number_str) != 10:
            raise PersonPhoneNumberException("Error! Romanian phone numbers should contain 10 digits!")
        if phone_number_str[0] not in valid_first_digits:
            raise PersonPhoneNumberException(f"Error! All romanian phone numbers begin with {valid_first_digits[0]}."
                                             f"\nThe digit {phone_number_str[0]} is not accepted as a first digit"
                                             f"in the Romanian format.")
        if phone_number_str[1] not in valid_second_digits:
            raise PersonPhoneNumberException(f"Error! Romanian phone numbers have one of the following as second "
                                             f"digits: {', '.join(valid_second_digits)}.\nThe digit"
                                             f"{phone_number_str[1]} is not accepted as a second digit in "
                                             f"the Romanian format")
        if phone_number_str[2] not in valid_third_digits:
            raise PersonPhoneNumberException(f"Error! Romanian phone numbers have one of the following as third"
                                             f"digits: {', '.join(valid_third_digits)}\nThe digit "
                                             f"{phone_number_str[2]} is not accepted as a third digit in "
                                             f"the Romanian format.")

        return f"{phone_number_str[:4]} {phone_number_str[4:7]} {phone_number_str[7:]}"


class PersonIDValidator:
    """
    Validator for the person ID input (coming from the user)
    """

    @staticmethod
    def validate(person_ids):
        """
        Checks if the given person IDs were given in an accepted format and then parses them into the format
        that the program will work with.
        :param person_ids: String or list of positive integers representing persons IDs
        :return passed_valid: The given inputs that could be interpreted as valid person IDs
        :return not_passed_valid: The given inputs that could NOT be interpreted as valid person IDs, each having
        an associated PersonIDException and a message describing why the input is invalid
        """

        if person_ids == [] or person_ids == '':
            return [], []

        if all(isinstance(id_, int) and id_ > 0 for id_ in person_ids):
            return person_ids, []
        elif all(isinstance(id_, int) for id_ in person_ids) and any(id_ < 0 for id_ in person_ids):
            passed_valid = [id_ for id_ in person_ids if id_ > 0]
            not_passed_valid = [PersonIDException(str(id_) + " - Error! Person IDs should be positive")
                                for id_ in person_ids if id_ <= 0]
            return passed_valid, not_passed_valid

        person_ids = person_ids.replace(' ', '')
        person_ids_list = person_ids.split(',')
        passed_valid = []
        not_passed_valid = []

        for pers_id in person_ids_list:
            try:
                int_id = int(pers_id)
            except ValueError:
                not_passed_valid.append(PersonIDException(pers_id + " - Error! Person IDs should be integers.\n"))
            else:
                if int_id <= 0:
                    not_passed_valid.append(PersonIDException(str(int_id) + " - Error! Person IDs should "
                                                                            "be positive.\n"))
                else:
                    passed_valid.append(int_id)

        return passed_valid, not_passed_valid


# ----------------- ACTIVITY VALIDATORS ----------------- #


class DateTimeValidator:
    """
    Validator for the date and time given by the user
    """

    @staticmethod
    def validate(date="", time=""):
        """
        Checks to see if the given date and time were given in an accepted format. If they were, they are
        converted into a representation that the program can work with.
        :param date: The year, month, and day given by the user; string
        :param time: The hour and minute given by the user; string
        :return: A datetime variable that acts as a representation of the given date and time that the program
        can work with
        :raise ActivityDateException: If invalid year, month, day, hour, or minute were given, or if a datetime
        from the past was given (you can't set events in the past, can you?)
        """
        if len(re.findall("[^0-9/: ]+", date)) or len(re.findall("[^0-9/: ]+", time)):
            raise ActivityDateException("Activity date should contain only digits(0-9), slashes(/), and colons(:).")

        if date == time == "":
            raise ActivityDateException("No date and time provided.")

        elif date != "" and time == "":
            try:
                day, month, year = map(int, date.strip().split('/'))
                date_year_month_day = datetime.date(year, month, day)
            except ValueError as ve:
                raise ActivityDateException(str(ve))
            return date_year_month_day

        elif date == "" and time != "":
            try:
                hour, minute = map(int, time.strip().split(':'))
                date_hour_minute = datetime.time(hour, minute)
            except ValueError as ve:
                raise ActivityDateException(str(ve))
            return date_hour_minute

        try:
            day, month, year = map(int, date.strip().split('/'))
            date_year_month_day = datetime.date(year, month, day)
        except ValueError as ve:
            raise ActivityDateException(str(ve))

        try:
            hour, minute = map(int, time.strip().split(':'))
            date_hour_minute = datetime.time(hour, minute)
        except ValueError as ve:
            raise ActivityDateException(str(ve))

        full_date_time = datetime.datetime.combine(date_year_month_day, date_hour_minute)
        return full_date_time


class ActivityIDValidator:
    """
    Validator for the activity ID given by the user
    """

    @staticmethod
    def validate(activity_id):
        """
        Checks to see if the activity ID given by the user was given in an accepted format (i.e., is a positive
        integer). If it is, it returns the parse activity ID.
        :param activity_id: The activity ID given by the user; string
        :return activity_id: The parsed and validated activity ID; positive integer
        """
        try:
            activity_id = int(activity_id)
        except ValueError:
            raise ActivityIDException("Activity ID must be an integer.")

        if activity_id <= 0:
            raise ActivityIDException("Activity ID must be a positive integer.")
        return activity_id
