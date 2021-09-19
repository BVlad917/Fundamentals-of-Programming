"""
The testing functions module. Everything test related is here.
"""
from copy import deepcopy

import src.domain.entity as domain
import src.functions.functions as fns


def set_up_test():
    """
    'Sets the stage' for the testing phase. Call this fn at the beginning of each testing fn

    :return students: A dummy variable; List of students made just for testing purposes
    """
    apartments = []
    new_apart = fns.occupy_new_apartment(apartments, 1)
    domain.set_apart_water_exp(new_apart, 100)
    domain.set_apart_heating_exp(new_apart, 200)
    domain.set_apart_gas_exp(new_apart, 300)
    domain.set_apart_electricity_exp(new_apart, 400)
    domain.set_apart_other_exp(new_apart, 500)

    new_apart = fns.occupy_new_apartment(apartments, 2)
    domain.set_apart_water_exp(new_apart, 50)
    domain.set_apart_heating_exp(new_apart, 75)
    domain.set_apart_gas_exp(new_apart, 100)
    domain.set_apart_electricity_exp(new_apart, 30)
    domain.set_apart_other_exp(new_apart, 40)

    new_apart = fns.occupy_new_apartment(apartments, 3)
    domain.set_apart_water_exp(new_apart, 10)
    domain.set_apart_heating_exp(new_apart, 70)
    domain.set_apart_gas_exp(new_apart, 90)
    domain.set_apart_electricity_exp(new_apart, 80)
    domain.set_apart_other_exp(new_apart, 20)

    return apartments


def test_parse_command():
    assert fns.parse_command_and_arguments("Add    17,  WATER,  250 RON.") == ("add", [17, "water", 250])
    assert fns.parse_command_and_arguments("Remove     25.") == ("remove", [25])
    assert fns.parse_command_and_arguments("   Remove 5    to  17.") == ("remove", [5, 17])
    assert fns.parse_command_and_arguments("Remove   THE   HEATING") == ("remove", ["heating"])
    assert fns.parse_command_and_arguments("   Replace 25  water with    200  RON") == ("replace", [25, "water", 200])
    assert fns.parse_command_and_arguments(" list     ") == ("list", [])
    assert fns.parse_command_and_arguments(" LIST    32") == ("list", [32])
    assert fns.parse_command_and_arguments("list   <     200") == ("list", ["<", 200])
    assert fns.parse_command_and_arguments("EXIT  ") == ("exit", [])
    assert fns.parse_command_and_arguments("sort apartment") == ("sort", ["apartment"])
    assert fns.parse_command_and_arguments("filter    gAs  ") == ("filter", ["gas"])
    assert fns.parse_command_and_arguments("  filter     300  ") == ("filter", [300])

    try:
        fns.parse_command_and_arguments("Add -20 water")
        assert False
    except ValueError:  # Cannot have negative numbers => ValueError
        assert True

    try:
        fns.parse_command_and_arguments("Remove   THE   phone")  # No expense called 'phone' => KeyError
        assert False
    except KeyError:
        assert True


def test_find_apartment_by_nr():
    apartments = set_up_test()
    assert (fns.find_apartment_by_nr(apartments, 1) is not None) and \
           (fns.find_apartment_by_nr(apartments, 2) is not None) and \
           (fns.find_apartment_by_nr(apartments, 3) is not None)

    assert fns.find_apartment_by_nr(apartments, 5) is None


def test_occupy_new_apartment():
    apartments = set_up_test()
    assert len(apartments) == 3
    fns.occupy_new_apartment(apartments, 4)
    assert len(apartments) == 4

    try:
        fns.occupy_new_apartment(apartments, -1)
        assert False
    except ValueError:
        assert True

    try:
        fns.occupy_new_apartment(apartments, domain.get_max_apart_nr() + 5)
        assert False
    except ValueError:
        assert True

    try:
        fns.occupy_new_apartment(apartments, 2)
        assert False
    except ValueError:
        assert True


def test_clear_apartment():
    apartments = set_up_test()

    fns.clear_apartment(apartments, 1)
    fns.clear_apartment(apartments, 2)

    assert len(apartments) == 1

    try:
        fns.clear_apartment(apartments, -1)
        assert False
    except ValueError:
        assert True

    try:
        fns.clear_apartment(apartments, domain.get_max_apart_nr() + 2)
        assert False
    except ValueError:
        assert True

    try:
        fns.clear_apartment(apartments, 5)
        assert False
    except ValueError:
        assert True


def test_add_expense():
    apartments = set_up_test()
    fns.add_expense(apartments, 1, 'water', 100)
    assert domain.get_apart_water_exp(apartments[0]) == 200
    assert domain.get_apart_total_exp(apartments[0]) == 1600

    try:
        fns.add_expense(apartments, 2, 'total', 50)
        assert False
    except KeyError:
        assert True

    try:
        fns.add_expense(apartments, 2, 'phone', 100)
        assert False
    except KeyError:
        assert True

    try:
        fns.add_expense(apartments, 1, 'gas', -50)
        assert False
    except ValueError:
        assert True

    try:
        fns.add_expense(apartments, 5, 'water', 100)
        assert False
    except ValueError:
        assert True

    fns.add_expense(apartments, 5, 'water', 100, talked_to_user=True)
    assert len(apartments) == 4


def test_remove_all_from_to():
    apartments = set_up_test()

    fns.remove_all_from_to(apartments, 1, 2)
    assert domain.get_apart_total_exp(apartments[0]) == domain.get_apart_total_exp(apartments[1]) == 0

    try:
        fns.remove_all_from_to(apartments, 205, 210)
        assert False
    except ValueError:
        assert True

    try:
        fns.remove_all_from_to(apartments, -10, -5)
        assert False
    except ValueError:
        assert True


def test_remove_all_expenses_from_apartment():
    apartments = set_up_test()
    try:
        fns.remove_all_expenses_from_apartment(apartments, 5)
        assert False
    except ValueError:
        assert True

    try:
        fns.remove_all_expenses_from_apartment(apartments, -5)
        assert False
    except ValueError:
        assert True

    try:
        fns.remove_all_expenses_from_apartment(apartments, domain.get_max_apart_nr() + 5)
        assert False
    except ValueError:
        assert True

    fns.remove_all_expenses_from_apartment(apartments, 1)
    assert domain.get_apart_total_exp(apartments[0]) == 0


def test_remove_all_type_expenses():
    apartments = set_up_test()
    try:
        fns.remove_all_type_expenses(apartments, 'phone')
        assert False
    except KeyError:
        assert True

    try:
        fns.remove_all_type_expenses(apartments, 'total')
        assert False
    except KeyError:
        assert True

    fns.remove_all_type_expenses(apartments, 'gas')
    assert domain.get_apart_gas_exp(apartments[0]) == \
           domain.get_apart_gas_exp(apartments[1]) == \
           domain.get_apart_gas_exp(apartments[2]) == 0

    # Check that the other expenses were not changed
    assert domain.get_apart_water_exp(apartments[0]) != 0 and \
           domain.get_apart_heating_exp(apartments[0]) != 0 and \
           domain.get_apart_other_exp(apartments[0]) != 0 and \
           domain.get_apart_electricity_exp(apartments[0]) != 0


def test_replace_expense():
    apartments = set_up_test()

    try:
        fns.replace_expense(apartments, 5, 'gas', 200)
        assert False
    except ValueError:
        assert True

    try:
        fns.replace_expense(apartments, 1, 'water', -100)
        assert False
    except ValueError:
        assert True

    try:
        fns.replace_expense(apartments, domain.get_max_apart_nr() + 5, 'water', 100)
        assert False
    except ValueError:
        assert True

    try:
        fns.replace_expense(apartments, 1, 'phone', 500)
        assert False
    except KeyError:
        assert True

    try:
        fns.replace_expense(apartments, 2, 'total', 100)
        assert False
    except KeyError:
        assert True

    fns.replace_expense(apartments, 1, 'water', 0)
    assert domain.get_apart_water_exp(apartments[0]) == 0
    assert domain.get_apart_total_exp(apartments[0]) == 1400


def test_get_expense_type_for_all_apartments():
    apartments = set_up_test()
    assert fns.get_expense_type_for_all_apartments(apartments, 'gas') == [(1, 300), (2, 100), (3, 90)]
    assert fns.get_expense_type_for_all_apartments(apartments, 'water') == [(1, 100), (2, 50), (3, 10)]
    try:
        fns.get_expense_type_for_all_apartments(apartments, 'phone')
        assert False
    except KeyError:
        assert True


def test_get_expenses_one_apartment():
    apartments = set_up_test()
    try:
        fns.get_expenses_one_apartment(apartments, -1)
        assert False
    except ValueError:
        assert True

    try:
        fns.get_expenses_one_apartment(apartments, domain.get_max_apart_nr() + 5)
        assert False
    except ValueError:
        assert True

    try:
        fns.get_expenses_one_apartment(apartments, 5)
        assert False
    except ValueError:
        assert True

    expenses_of_apart1 = fns.get_expenses_one_apartment(apartments, 1)
    values_of_expenses_of_apart1 = [expense[1] for expense in expenses_of_apart1]

    # We also have to take into consideration that the total expense will also be returned in the list
    assert sorted(values_of_expenses_of_apart1) == [100, 200, 300, 400, 500, 1500]


def test_get_totals_with_condition():
    apartments = set_up_test()
    try:
        fns.get_totals_with_condition(apartments, '>=', 100)
        assert False
    except ValueError:
        assert True

    try:
        fns.get_totals_with_condition(apartments, '>', -100)
        assert False
    except ValueError:
        assert True

    sorted_filtered_apartments = fns.get_totals_with_condition(apartments, '>', 280)
    values_sorted_filtered_apartments = [apart[1] for apart in sorted_filtered_apartments]
    assert values_sorted_filtered_apartments == [1500, 295]

    sorted_filtered_apartments = fns.get_totals_with_condition(apartments, '<', 10)
    assert len(sorted_filtered_apartments) == 0


def test_sum_expense_type():
    apartments = set_up_test()
    assert fns.sum_expense_type(apartments, 'gas') == 490
    try:
        fns.sum_expense_type(apartments, 'phone')
        assert False
    except KeyError:
        assert True


def test_sorted_ascending_apartments():
    apartments = set_up_test()
    sorted_by_totals = fns.sorted_ascending_apartments_totals(apartments)
    assert sorted_by_totals == [(3, 270), (2, 295), (1, 1500)]


def test_sorted_expense_types():
    apartments = set_up_test()
    sorted_expenses = fns.sorted_expense_types(apartments)
    assert sorted_expenses == [('water', 160), ('heating', 345), ('gas', 490), ('electricity', 510), ('other', 560)]


def test_max_apartment_expense():
    apartments = set_up_test()
    assert fns.max_apartment_expense(apartments, 1) == ('other', 500)
    assert fns.max_apartment_expense(apartments, 2) == ('gas', 100)
    assert fns.max_apartment_expense(apartments, 3) == ('gas', 90)

    try:
        fns.max_apartment_expense(apartments, 4)
        assert False
    except ValueError:
        assert True

    try:
        fns.max_apartment_expense(apartments, -5)
        assert False
    except ValueError:
        assert True


def test_filter_by_expense_type():
    apartments = set_up_test()

    fns.filter_by_expense_type(apartments, 'gas')
    assert domain.get_apart_gas_exp(apartments[0]) != 0 and \
           domain.get_apart_gas_exp(apartments[1]) != 0 and \
           domain.get_apart_gas_exp(apartments[2]) != 0

    # Test that all expenses except 'gas' have been removed
    assert domain.get_apart_total_exp(apartments[0]) == domain.get_apart_gas_exp(apartments[0])
    assert domain.get_apart_total_exp(apartments[1]) == domain.get_apart_gas_exp(apartments[1])
    assert domain.get_apart_total_exp(apartments[2]) == domain.get_apart_gas_exp(apartments[2])

    try:
        fns.filter_by_expense_type(apartments, 'phone')
        assert False
    except KeyError:
        assert True


def test_filter_by_value():
    apartments = set_up_test()
    fns.filter_by_value(apartments, 100)

    # Test that all expenses of the first apartment have been set to 0, since apartment 1 had all expenses >= 100
    # In the other 2 apartments, only some/none of the expenses have been modified
    assert domain.get_apart_total_exp(apartments[0]) == 0
    assert domain.get_apart_total_exp(apartments[1]) == 195
    assert domain.get_apart_total_exp(apartments[2]) == 270

    try:
        fns.filter_by_value(apartments, -5)
        assert False
    except ValueError:
        assert True


def test_check_state_change():
    apartments = set_up_test()
    current_state = deepcopy(apartments)
    states = []

    fns.add_expense(apartments, 1, 'water', 100)

    current_state = fns.check_state_change(apartments, states, current_state)
    assert len(states) == 1

    fns.add_expense(apartments, 2, 'gas', 200)
    current_state = fns.check_state_change(apartments, states, current_state)
    assert len(states) == 2

    fns.replace_expense(apartments, 3, 'gas', 150)
    current_state = fns.check_state_change(apartments, states, current_state)
    assert len(states) == 3

    assert current_state == apartments


def test_undo():
    apartments = set_up_test()
    current_state = deepcopy(apartments)
    states = []

    initial_state = deepcopy(apartments)

    fns.add_expense(apartments, 1, 'water', 50)
    current_state = fns.check_state_change(apartments, states, current_state)
    state_after_change1 = deepcopy(current_state)

    fns.add_expense(apartments, 2, 'gas', 200)
    current_state = fns.check_state_change(apartments, states, current_state)
    state_after_change2 = deepcopy(current_state)

    fns.replace_expense(apartments, 3, 'gas', 150)
    current_state = fns.check_state_change(apartments, states, current_state)

    apartments, current_state = fns.undo(apartments, states, current_state)
    assert apartments == current_state == state_after_change2

    apartments, current_state = fns.undo(apartments, states, current_state)
    assert apartments == current_state == state_after_change1

    apartments, current_state = fns.undo(apartments, states, current_state)
    assert apartments == current_state == initial_state

    try:
        fns.undo(apartments, states, current_state)
        assert False
    except ValueError:
        assert True


def run_all_tests():
    test_get_totals_with_condition()
    test_get_expenses_one_apartment()
    test_get_expense_type_for_all_apartments()
    test_replace_expense()
    test_remove_all_type_expenses()
    test_remove_all_expenses_from_apartment()
    test_remove_all_from_to()
    test_add_expense()
    test_clear_apartment()
    test_find_apartment_by_nr()
    test_occupy_new_apartment()
    test_parse_command()
    test_sum_expense_type()
    test_sorted_ascending_apartments()
    test_sorted_expense_types()
    test_max_apartment_expense()
    test_filter_by_expense_type()
    test_filter_by_value()
    test_check_state_change()
    test_undo()
    test_undo()
