"""
    Module for testing the functionalities of the program
"""

from src.domain.entity import ComplexNumber
from src.domain.validators import InputValidator, FilteringValidator, AddComplexNumValidator, FilteringException, \
    ComplexNumException
from src.services.service import ListService


# -------------------------------------------------- #
# -------------- COMPLEX NUMBER TESTS -------------- #
# -------------------------------------------------- #


def test_complex_number_representation():
    a = ComplexNumber(5, 2)
    assert a.real == 5 and a.imag == 2

    a = ComplexNumber(2, -2)
    assert a.real == 2 and a.imag == -2
    assert repr(a) == '2-2i'

    a = ComplexNumber(2)
    assert a.real == 2 and a.imag == 0
    assert repr(a) == '2'

    a = ComplexNumber(imag=-1)
    assert a.real == 0 and a.imag == -1
    assert repr(a) == '-i'

    a = ComplexNumber(imag=1)
    assert a.real == 0 and a.imag == 1
    assert repr(a) == 'i'

    a = ComplexNumber(5, 2)
    b = ComplexNumber(5, 2)
    assert a == b


# -------------------------------------------------------- #
# -------------- LIST SERVICE METHODS TESTS -------------- #
# -------------------------------------------------------- #


def test_list_service_representation():
    add_validator = AddComplexNumValidator()
    filter_validator = FilteringValidator()

    service = ListService(add_validator, filter_validator)
    service.fill_list()  # Now the list has 10 random complex numbers

    assert len(service) == 10
    service.add_number(2, 2)
    assert len(service) == 11

    assert ComplexNumber(2, 2) in service
    # Test that the list service is iterable
    for _ in service:
        pass


def test_list_service_add_num():
    add_validator = AddComplexNumValidator()
    filter_validator = FilteringValidator()

    service = ListService(add_validator, filter_validator)
    service.fill_list()  # Now the list has 10 random complex numbers

    assert len(service) == 10
    service.add_number(2, 2)
    assert len(service) == 11

    try:
        service.add_number(2, 2)
        assert False
    except ComplexNumException:
        assert True


def test_list_service_find_num():
    add_validator = AddComplexNumValidator()
    filter_validator = FilteringValidator()

    service = ListService(add_validator, filter_validator)
    service.fill_list()  # Now the list has 10 random complex numbers

    service.add_number(2, 2)
    assert service.find_num(ComplexNumber(2, 2)) == 10


def test_list_service_fill_list():
    add_validator = AddComplexNumValidator()
    filter_validator = FilteringValidator()

    service = ListService(add_validator, filter_validator)
    service.fill_list()  # Now the list has 10 random complex numbers

    assert len(service) == 10
    service.fill_list(n=20)
    assert len(service) == 30


def test_list_service_filter():
    add_validator = AddComplexNumValidator()
    filter_validator = FilteringValidator()

    service = ListService(add_validator, filter_validator)
    service.fill_list(20)  # Now the list has 20 random complex numbers
    assert len(service) == 20

    service.filter(1, 10)
    assert len(service) == 10
    service.filter(2, 20)
    assert len(service) == 9
    service.filter(-5, 5)
    assert len(service) == 5
    service.filter(4, 1)
    assert len(service) == 4

    try:
        service.filter(10, 20)
        assert False
    except FilteringException:
        assert True
    try:
        service.filter(-5, -2)
        assert False
    except FilteringException:
        assert True


# ---------------------------------------------- #
# -------------- VALIDATORS TESTS -------------- #
# ---------------------------------------------- #


def test_input_validator():
    input_validator = InputValidator()
    assert input_validator.validate('5+2i') == (5, 2)
    assert input_validator.validate('5-2i') == (5, -2)
    assert input_validator.validate('  5 +    2i ') == (5, 2)
    assert input_validator.validate('   5   +    2   i') == (5, 2)
    assert input_validator.validate('  2i ') == (0, 2)
    assert input_validator.validate('   -2 i   ') == (0, -2)
    assert input_validator.validate('5') == (5, 0)
    assert input_validator.validate('    - 5') == (-5, 0)
    assert input_validator.validate('i') == (0, 1)
    assert input_validator.validate('-i') == (0, -1)

    try:
        input_validator.validate('5 +3i +    10')
        assert False
    except ValueError:
        assert True

    try:
        input_validator.validate('5i +3i')
        assert False
    except ValueError:
        assert True


def test_filter_validator():
    add_validator = AddComplexNumValidator()
    filter_validator = FilteringValidator()

    service = ListService(add_validator, filter_validator)
    service.fill_list()  # The valid indices for filter must be between 1 and 10
    assert len(service) == 10

    service.filter(2, 8)
    assert len(service) == 7

    service.filter(2, 200)
    assert len(service) == 6

    service.filter(-5, 4)
    assert len(service) == 4

    service.filter(4, 2)
    assert len(service) == 3

    try:
        service.filter(5, 10)
        assert False
    except FilteringException:
        assert True

    try:
        service.filter(-5, -2)
        assert False
    except FilteringException:
        assert True


def test_add_complex_num_validator():
    add_validator = AddComplexNumValidator()
    filter_validator = FilteringValidator()

    service = ListService(add_validator, filter_validator)
    service.fill_list()  # Now the list has 10 random complex numbers
    assert len(service) == 10

    service.add_number(200, 2)
    assert len(service) == 11

    service.add_number(200, -2)
    assert len(service) == 12

    try:
        service.add_number(200, 2)
        assert False
    except ComplexNumException:
        assert True


def test_list_service_undo():
    add_validator = AddComplexNumValidator()
    filter_validator = FilteringValidator()

    service = ListService(add_validator, filter_validator)
    service.fill_list()  # Now the list has 10 random complex numbers
    assert len(service) == 10

    service.add_number(2, 2)
    assert len(service) == 11
    service.undo()
    assert len(service) == 10

    service.filter(2, 6)
    assert len(service) == 5
    service.undo()
    assert len(service) == 10

    try:
        service.undo()
        assert False
    except ValueError:
        assert True


def test_all():
    test_complex_number_representation()
    test_input_validator()
    test_filter_validator()
    test_add_complex_num_validator()
    test_list_service_representation()
    test_list_service_find_num()
    test_list_service_fill_list()
    test_list_service_filter()
    test_list_service_add_num()
    test_list_service_undo()
