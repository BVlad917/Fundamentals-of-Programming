"""
The domain module. Domain file includes code for entity management.
In this case, the entity is the apartment.
"""


def create_apartment(apart_nr):
    """
    Creates an apartment with no expenses. Every apartment will be an individual object. Its keys will be the
    apartment number, the maximum apartment number accepted (notice we keep this number close to the definition
    of an apartment, as we will need it very frequently, so we don't drag it along every function as a parameter),
    a dictionary with all the expenses and the forth and final key will be the total expenses (sum of the
    dictionary of expenses)
    :param apart_nr: The apartment number we want our new apartment to have; positive integer
    :return: The newly created apartment; dictionary
    """
    max_apart_number = 200

    return {'apart_nr': apart_nr, 'max_apart_nr': max_apart_number, 'total': 0, 'expenses': {
        'water': 0, 'heating': 0, 'gas': 0, 'electricity': 0, 'other': 0
    }}


# ----------------------- #
# ------- GETTERS ------- #
# ----------------------- #


def get_max_apart_nr():
    """
    Returns the maximum apartment number accepted
    """
    dummy_apartment = create_apartment(-1)  # Dummy apartment variable; only used to get <max_apart_nr>
    return dummy_apartment['max_apart_nr']


def get_available_expenses():
    """
    Returns the currently available expense types as a list of strings.
    Note: The 'total' expenses will not be included in this list
    """
    dummy_apartment = create_apartment(-1)
    return [*dummy_apartment['expenses'].keys()]  # Returns as list, not dict_keys


def get_all_expenses_of_apart(apart):
    """
    Returns the dictionary of all of the apartment's expenses
    """
    return apart['expenses']


def get_apart_nr(apart):
    """
    Returns the apartment's number
    """
    return apart['apart_nr']


def get_any_expense(apart, expense_type):
    """
    Returns the <type> expense of the apartment.

    :param apart: The apartment whose <type> expense we want to return; dictionary
    :param expense_type: The type of expense; string
    """
    if expense_type != 'total':
        return apart['expenses'][expense_type]
    return apart['total']


def get_apart_water_exp(apart):
    """
    Returns the apartment's water expense
    """
    return apart['expenses']['water']


def get_apart_heating_exp(apart):
    """
    Returns the apartment's heating expense
    """
    return apart['expenses']['heating']


def get_apart_electricity_exp(apart):
    """
    Returns the apartment's electricity expense
    """
    return apart['expenses']['electricity']


def get_apart_gas_exp(apart):
    """
    Returns the apartment's gas expense
    """
    return apart['expenses']['gas']


def get_apart_other_exp(apart):
    """
    Returns the apartment's other expenses
    """
    return apart['expenses']['other']


def get_apart_total_exp(apart):
    """
    Returns the apartment's total expenses
    """
    return apart['total']


# ----------------------- #
# ------- SETTERS ------- #
# ----------------------- #


def set_apart_nr(apart, nr):
    """
    Sets the apartment's number.

    :param apart: The apartment whose number we want to change; dictionary
    :param nr: The new number we want the apartment to have; positive integer
    """
    apart['apart_nr'] = nr


def set_any_expense(apart, exp_type, exp_amount):
    """
    Sets the <type> expense to the amount <exp>.

    :param apart: The apartment we want to set an expense to; dictionary
    :param exp_type: The type of expense; string
    :param exp_amount: The expense amount; positive integer
    """
    apart['expenses'][exp_type] = exp_amount
    update_total_expenses(apart)


def set_apart_water_exp(apart, exp):
    """
    Sets the apartment's water expense

    :param apart: The apartment whose water expense we want to set; dictionary
    :param exp: The expense we want to set to water; positive integer
    """
    apart['expenses']['water'] = exp
    update_total_expenses(apart)


def set_apart_heating_exp(apart, exp):
    """
    Sets the apartment's heating expense

    :param apart: The apartment whose heating expense we want to set; dictionary
    :param exp: The expense we want to set to heating; positive integer
    """
    apart['expenses']['heating'] = exp
    update_total_expenses(apart)


def set_apart_electricity_exp(apart, exp):
    """
    Sets the apartment's electricity expense

    :param apart: The apartment whose electricity expense we want to set; dictionary
    :param exp: The expense we want to set to electricity; positive integer
    """
    apart['expenses']['electricity'] = exp
    update_total_expenses(apart)


def set_apart_gas_exp(apart, exp):
    """
    Sets the apartment's gas expense

    :param apart: The apartment whose gas expense we want to set; dictionary
    :param exp: The expense we want to set to gas; positive integer
    """
    apart['expenses']['gas'] = exp
    update_total_expenses(apart)


def set_apart_other_exp(apart, exp):
    """
    Sets the apartment's other expenses

    :param apart: The apartment whose other's expense we want to set; dictionary
    :param exp: The new expense we want to set to other's; positive integer
    """
    apart['expenses']['other'] = exp
    update_total_expenses(apart)


def set_apart_total_exp(apart, exp):
    """
    Only use this in the function that updates the apartment's total expenses.

    :param apart:
    :param exp:
    :return:
    """
    apart['total'] = exp


def set_all_expenses(apart, exp_amount):
    """
    Sets all of the apartment's expenses values to <exp>

    :param apart: The apartment whose expenses we want to set; dictionary
    :param exp_amount: The new expense we want to set to other's; positive integer
    """
    for expense_type in apart['expenses'].keys():
        set_any_expense(apart, expense_type, exp_amount)
    update_total_expenses(apart)


# ------------------------------- #
# ------- UPDATE FUNCTION ------- #
# ------------------------------- #


def update_total_expenses(apartment):
    """
    Updates the apartment's total expenses

    :param apartment: The apartment whose total expenses we want to update; dictionary
    """
    expenses_sum = sum(apartment['expenses'].values())
    set_apart_total_exp(apartment, expenses_sum)
