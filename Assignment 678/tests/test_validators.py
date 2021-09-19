import datetime
import unittest

from domain.validators import PhoneNumberValidator, PersonPhoneNumberException, PersonIDValidator, DateTimeValidator, \
    ActivityDateException, ActivityIDValidator, ActivityIDException, ActivityPersonException, ConsoleException, \
    ConsoleCommandException, UndoRedoException


class TestPhoneNumberValidator(unittest.TestCase):
    def setUp(self):
        self.phone_num_validator_fn = PhoneNumberValidator.validate

    def test_valid_and_parse_phone_numbers(self):
        self.assertEqual(self.phone_num_validator_fn('0745000111'), '0745 000 111')
        self.assertEqual(self.phone_num_validator_fn('0221014567'), '0221 014 567')
        self.assertEqual(self.phone_num_validator_fn('+40745123456'), '0745 123 456')
        self.assertEqual(self.phone_num_validator_fn('0734-090-464'), '0734 090 464')
        self.assertRaises(PersonPhoneNumberException, self.phone_num_validator_fn, '07345134a9')
        self.assertRaises(PersonPhoneNumberException, self.phone_num_validator_fn, '072123348')
        self.assertRaises(PersonPhoneNumberException, self.phone_num_validator_fn, '0713487497')
        self.assertRaises(PersonPhoneNumberException, self.phone_num_validator_fn, '1234567891')
        self.assertRaises(PersonPhoneNumberException, self.phone_num_validator_fn, '0934567891')


# ------------------------------------------------------------------------------------------ #
# ---------------------------------- TESTS FOR VALIDATORS ---------------------------------- #
# ------------------------------------------------------------------------------------------ #

class TestPersonIDValidator(unittest.TestCase):
    def setUp(self):
        self.person_id_validator_fn = PersonIDValidator.validate

    def test_valid_and_parse_person_ids(self):
        self.assertEqual(self.person_id_validator_fn(''), ([], []))
        self.assertEqual(self.person_id_validator_fn('1,2  , 4, 8'), ([1, 2, 4, 8], []))
        passed, not_passed = self.person_id_validator_fn('1, a, 3, 5, bc, -15')
        self.assertEqual(passed, [1, 3, 5])  # [1, 3, 5] will pass the validator fns
        self.assertEqual(len(not_passed), 3)  # ['a', 'bc'] won't pass the validator fns

        passed, not_passed = self.person_id_validator_fn([1, 2, 3, -4])
        self.assertEqual(len(not_passed), 1)
        self.assertEqual(passed, [1, 2, 3])

        passed, not_passed = self.person_id_validator_fn([1, 2, 3, 4])
        self.assertEqual(passed, [1, 2, 3, 4])
        self.assertEqual(not_passed, [])


class TestDateTimeValidator(unittest.TestCase):
    def setUp(self):
        self.datetime_validator_fn = DateTimeValidator.validate

    def test_valid_and_parse_datetime(self):
        dt = self.datetime_validator_fn('17/5/2001', '20:00:00')
        self.assertEqual(dt, datetime.datetime(2001, 5, 17, 20, 0))

        self.assertRaises(ActivityDateException, self.datetime_validator_fn, '30/2/2010', '12:00')
        self.assertRaises(ActivityDateException, self.datetime_validator_fn, '15/2/2010', '24:30')

        self.assertRaises(ActivityDateException, self.datetime_validator_fn, 'asg34tg', 'nonsense2')
        self.assertRaises(ActivityDateException, self.datetime_validator_fn)
        date_year_month_day = self.datetime_validator_fn(date='15/6/2020')
        self.assertEqual(date_year_month_day, datetime.date(2020, 6, 15))
        date_hour_minute = self.datetime_validator_fn(time='15:30')
        self.assertEqual(date_hour_minute, datetime.time(15, 30))

        self.assertRaises(ActivityDateException, self.datetime_validator_fn, date='132/4234/412312')
        self.assertRaises(ActivityDateException, self.datetime_validator_fn, time='27:89')


class TestActivityIDValidator(unittest.TestCase):
    def setUp(self):
        self.activity_id_validator_fn = ActivityIDValidator.validate

    def test_valid_and_parse_activity_id(self):
        self.assertEqual(self.activity_id_validator_fn('5'), 5)
        self.assertEqual(self.activity_id_validator_fn(7), 7)

        self.assertRaises(ActivityIDException, self.activity_id_validator_fn, 'xyz')
        self.assertRaises(ActivityIDException, self.activity_id_validator_fn, '-5')


class TestExceptions(unittest.TestCase):
    def setUp(self):
        self.activity_person_exception_class = ActivityPersonException
        self.console_exception_class = ConsoleException
        self.console_command_exception_class = ConsoleCommandException
        self.undo_redo_exc_class = UndoRedoException

    def test_exception_inheritance(self):
        self.assertTrue(issubclass(self.activity_person_exception_class, Exception))
        self.assertTrue(issubclass(self.console_command_exception_class, Exception))
        self.assertTrue(issubclass(self.console_command_exception_class, Exception))

    def test_exception_instantiation(self):
        act_pers_exc = self.activity_person_exception_class("Activity Person Exception")
        console_ex = self.console_exception_class("Console Exception")
        console_command_exc = self.console_command_exception_class("Console Command Exception")
        undo_redo_exc = self.undo_redo_exc_class("Undo/Redo Exception")
        self.assertIsInstance(act_pers_exc, ActivityPersonException)
        self.assertIsInstance(console_ex, ConsoleException)
        self.assertIsInstance(console_command_exc, ConsoleCommandException)
        self.assertIsInstance(undo_redo_exc, UndoRedoException)
