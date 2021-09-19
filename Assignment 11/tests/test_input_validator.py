import unittest

from errors.board_exceptions import InvalidInputData
from validation.input_data_validator import InputDataValidator


class TestInputValidator(unittest.TestCase):
    def test_validate(self):
        validator = InputDataValidator()
        self.assertRaises(InvalidInputData, validator.validate, 9)
        self.assertEqual(validator.validate(6), 6)