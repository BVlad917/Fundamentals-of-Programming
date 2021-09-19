"""
The functions module. These functions (or operations) implement the program features.
They call each other, or other functions from the domain
"""

from copy import deepcopy
from random import sample, randint

import src.domain.entity as domain


def find_apartment_by_nr(apartments, apart_nr):
    """
    Checks to see if the 'apart_nr' apartment number is currently occupied. If it is, the function returns this
    apartment

    :param apartments: The list of apartments; list of dictionaries
    :param apart_nr: The number of the apartment to search for; positive integer
    :return: The apartment from the list of apartments that 'apart_nr' occupies IF found (in this case, returns dict);
    Returns None if 'apart_nr' not occupied
    """
    res = list(filter(lambda x: domain.get_apart_nr(x) == apart_nr, apartments))
    return res[0] if len(res) > 0 else None


def occupy_new_apartment(apartments, apart_nr):
    """
    Adds a new apartment, with 'apart_nr' as the new apartment's number

    :param apartments: The list of apartments; list of dictionaries
    :param apart_nr: The number we want the newly added apartment to have; positive integer <= max_apart_nr
    :return: -
    :raise ValueError: if apart_nr is not a positive integer, is greater than 200, or if that apartment number
    is already occupied.
    """
    if apart_nr <= 0:
        raise ValueError("The apartment number needs to be a positive integer!")

    max_apart_nr = domain.get_max_apart_nr()
    if apart_nr > max_apart_nr:
        raise ValueError("We don't have that many apartments! Maximum is {}.".format(max_apart_nr))

    if find_apartment_by_nr(apartments, apart_nr) is not None:
        raise ValueError("This apartment is occupied! Try a different apartment number.")

    new_apartment = domain.create_apartment(apart_nr)
    apartments.append(new_apartment)
    return new_apartment


def clear_apartment(apartments, apart_nr):
    """
    Clears an apartment, removing it from the list (and, implicitly, setting all expenses to 0)

    :param apartments: The list of apartments; list of dictionaries
    :param apart_nr: The number of the apartment to be cleared
    :raise: ValueError if: The number of the apartment to be cleared is not a positive integer in the
    interval [0, <max_apart_nr>]; if the apartment is not occupied (i.e., it's already cleared)
    """

    if apart_nr <= 0:
        raise ValueError("The apartment number must be a positive integer!")

    max_apart_nr = domain.get_max_apart_nr()
    if apart_nr > max_apart_nr:
        raise ValueError("We don't have that many apartments! Maximum is {}.".format(max_apart_nr))

    apartment_to_remove = find_apartment_by_nr(apartments, apart_nr)
    if apartment_to_remove is None:
        raise ValueError(f"Apartment {apart_nr} is not occupied. Nothing to clear.")

    apartments.remove(apartment_to_remove)
    return apartment_to_remove


def clear_range_of_apartments(apartments, start_apart_nr, end_apart_nr):
    """
    Applies the 'clear_apartment()' function over the range of apartments [<start_apart_nr>, <end_apart_nr>]

    :param apartments: The list of apartments; list of dictionaries
    :param start_apart_nr: The lower bound of the interval of apartments to clear
    :param end_apart_nr: The upper bound of the interval of apartments to clear
    """
    for apart_nr in range(start_apart_nr, end_apart_nr + 1):
        try:
            clear_apartment(apartments, apart_nr)
        except ValueError:
            continue


def fill_random_apartments(apartments, nr_of_apartments=10, exp_lb=1, exp_ub=1000):
    """
    Fills 'nr_of_apartments' random apartments with random expenses

    :param apartments: The list of apartments; list of dictionaries
    :param nr_of_apartments: How many apartments to fill; positive integer
    :param exp_lb: The expenses lower bound to fill; positive integer
    :param exp_ub: The expenses upper bound to fill; positive integer
    :return: -
    :raise ValueError: if <number_of_apartments>, <expense_lower_bound>, or <expense_upper_bound> are negative
    :raise KeyError: if given a currently not available expense
    """

    if nr_of_apartments <= 0 or exp_lb <= 0 or exp_ub <= 0:
        raise ValueError("Apartment numbers and expense values must be positive integers!")

    max_apart_nr = domain.get_max_apart_nr()
    available_expense_types = domain.get_available_expenses()
    apart_nrs = sample(range(1, max_apart_nr + 1), nr_of_apartments)

    for apart_nr in apart_nrs:
        new_apartment = occupy_new_apartment(apartments, apart_nr)
        for exp_type in available_expense_types:
            new_exp = randint(exp_lb, exp_ub)
            domain.set_any_expense(new_apartment, exp_type, new_exp)


def parse_input(cmd_line):
    """
    Parses the user input into a concise representation of the desired command
    Will extract the user's command and the arguments provided by the user for this command (if any)

    :param cmd_line: The string given by the user; We'll extract the command from this
    :return: Tuple containing a concise representation of the user's desired command
    """

    cmd_line = cmd_line.lower().strip()
    space_pos = cmd_line.find(' ')

    if space_pos == -1:  # if command is 'list', 'exit', or 'info'
        return cmd_line, []

    cmd = cmd_line[:space_pos]  # main command
    args = cmd_line[space_pos:]  # arguments for command

    # replace all unwanted characters with a space, which will be removed later
    for unwanted_char in [',', '.', '!', '?', ';', '- ', '`', '~', 'ron']:
        args = args.replace(unwanted_char, ' ')

    args = args.split(' ')

    # remove words that bind arguments (i.e., 'to', 'with', '' -> no character)
    args = [arg for arg in args if arg not in ['to', 'with', 'the', 'so', '']]

    return cmd, args


def parse_1_args(args):
    """
    Parses the arguments in the case of a command that can have just one argument

    :param args: The argument as a string in a list (e.g., ['25'], or ['water'])
    :return: The parsed argument in a list. It can now be used by the program (e.g., [25], or ['water']); list
    :raise ValueError: if given float numbers
    :raise KeyError: if given garbage as expense
    """

    available_expenses = domain.get_available_expenses()

    err_msg = "The command given expects a positive integer."
    try:
        args[0] = int(args[0])
    except ValueError:
        if any(char.isdigit() for char in args[0]):
            raise ValueError(err_msg)
        # If we're here, the only things args[0] could be is an expense or one of the strings 'apartment' or 'type'
        elif args[0] not in available_expenses + ['apartment', 'type']:
            raise KeyError("There is no available expense called '{}'.".format(args[0]))

    if isinstance(args[0], int) and args[0] <= 0:
        raise ValueError(err_msg)


def parse_2_args(args):
    """
    Parses the arguments in the case of a command that can have two arguments

    :param args: The arguments as string in a list (e.g., ['5', '12']); list of strings
    :return: The parsed arguments in a list. They can now be used by the program (e.g., [5, 12])
    :raise ValueError: if garbage instead of comparison sign, given float values, given non-positive integers
    """
    err_msg = "Apartment numbers and expense amount must be positive integers!"
    try:
        args[0] = int(args[0])
    except ValueError:
        if args[0] not in ['<', '=', '>']:
            if not any([char.isdigit() for char in args[0]]):
                raise ValueError("We only support equality or strict inequalities!")
            else:
                raise ValueError(err_msg)

    try:
        args[1] = int(args[1])
    except ValueError:
        raise ValueError(err_msg)

    if ((isinstance(args[0], int) and isinstance(args[1], int) and (args[0] <= 0 or args[1] <= 0) or
         (isinstance(args[1], int) and args[1] <= 0))):
        raise ValueError(err_msg)


def parse_3_arguments(args):
    """
     Parses the arguments in the case of a command that can have two arguments

    :param args: The arguments as strings in a list (e.g., ['5', 'water', '250'])
    :return: The parsed arguments in a list. They can now be used by the program (e.g., [5, 'water', 250])
    :raise ValueError: if garbage/negative integers are given instead of the expected positive integers
    :raise KeyError: if unavailable expense given as argument
    """
    available_expenses = domain.get_available_expenses()
    err_msg = "Apartment numbers and expense amount must be positive integers!"

    try:
        args[0] = int(args[0])
        args[2] = int(args[2])
    except ValueError:
        raise ValueError(err_msg)

    if args[0] <= 0 or args[2] <= 0:
        raise ValueError(err_msg)

    if args[1] not in available_expenses:
        raise KeyError("There is no available expense called '{}'.".format(args[1]))


def parse_command_and_arguments(cmd_line):
    """
    Takes in the parsed input from the parse_input() function and, according to the command, parses the individual
    arguments that were given in a format that is digestible for the program

    :param cmd_line: The given command line, coming directly from the user; string
    :return: The arguments in a format that can be used by the code (for example, ('add', [25, 'water', 250]))
    :raise ValueError: if too many arguments have been provided
    """
    cmd, args = parse_input(cmd_line)
    if len(args) >= 4:
        raise ValueError("Too many arguments given!")

    if len(args) == 1:
        parse_1_args(args)
    elif len(args) == 2:
        parse_2_args(args)
    elif len(args) == 3:
        parse_3_arguments(args)

    return cmd, args


def check_available_expense(expense_type):
    """
    Raises a KeyError if expense type <expense_type> is not currently available.

    :param expense_type: The expense we want to check; string
    """

    if expense_type not in domain.get_available_expenses():
        raise KeyError(f"The expense '{expense_type}' is not currently available in the list of expenses!")


def check_not_total(expense_type):
    """
    Raises a KeyError if the expenses type <expense_type> is 'total'. Used for making sure we don't change
    the total, which changes only when we change some other expense (and it does so automatically)

    :param expense_type: The expense we want to check; string
    """

    if expense_type == 'total':
        raise KeyError(f"You cannot change the total expenses directly.")


def add_expense(apartments, apart_nr, expense_type, expense_amount, talked_to_user=False):
    """
    Adds a new expense to an apartment

    :param apartments: The list of apartments; list of dictionaries
    :param apart_nr: The number of the apartment to add an expense to; positive integer
    :param expense_type: The type of the expense we want to add; string
    :param expense_amount: The amount of the expense we want to add; positive integer
    :param talked_to_user: Bool value. This variable only makes a difference in the case that the user tries
    to add an expense to an unoccupied apartment. In this case, if <talked_to_user> is set to True then the
    apartment will be occupied and the expense will be added to it. On the other hand, if <talked_to_user> is False,
    then no action will be taken.

    :raise ValueError: if expense amount is not positive
    :raise KeyError: if unavailable expense type given as argument
    """
    check_not_total(expense_type)
    check_available_expense(expense_type)

    if expense_amount <= 0:
        raise ValueError("Apartment number and expense amount must be positive integers!")

    apart_to_add_to = find_apartment_by_nr(apartments, apart_nr)

    if apart_to_add_to is None and talked_to_user is False:
        raise ValueError("This apartment is not occupied.")

    if apart_to_add_to is None and talked_to_user is True:
        apart_to_add_to = occupy_new_apartment(apartments, apart_nr)

    current_exp_amount = domain.get_any_expense(apart_to_add_to, expense_type)
    new_expense_amount = current_exp_amount + expense_amount
    domain.set_any_expense(apart_to_add_to, expense_type, new_expense_amount)


def remove_all_from_to(apartments, start_ap_nr, end_ap_nr):
    """
    Removes all expenses from all apartments from apartment number <start_ap_nr> to apartment number <end_ap_nr>
    (including these two)

    :param apartments: The list of all apartments, list of dictionaries
    :param start_ap_nr: The left bound of the interval of apartments to remove all expenses of
    :param end_ap_nr: The left right of the interval of apartments to remove all expenses of
    :returns: (<start_ap_nr>, <end_ap_nr>) tuple representing the interval of apartments whose
    expenses have been cleared
    """
    max_apartments = domain.get_max_apart_nr()

    if start_ap_nr > end_ap_nr:
        start_ap_nr, end_ap_nr = end_ap_nr, start_ap_nr  # Swap the order if not already increasing

    if (start_ap_nr <= 0 and end_ap_nr <= 0) or (start_ap_nr > max_apartments and end_ap_nr > max_apartments):
        raise ValueError("Please input apartment numbers between 1 and {}.".format(max_apartments))

    start_ap_nr = max(1, start_ap_nr)
    end_ap_nr = min(200, end_ap_nr)

    for apart_nr in range(start_ap_nr, end_ap_nr + 1):
        apartment = find_apartment_by_nr(apartments, apart_nr)

        if apartment is not None:
            domain.set_all_expenses(apartment, 0)

    return start_ap_nr, end_ap_nr


def remove_all_expenses_from_apartment(apartments, apartment_nr):
    """
    Removes all expenses from the apartment with apartment number <apartment_nr>

    :param apartments: The list of apartments; list of dictionaries
    :param apartment_nr: The apartment number whose expenses we want to remove
    """
    if apartment_nr <= 0 or apartment_nr > domain.get_max_apart_nr():
        raise ValueError(f"Apartment numbers must be positive integers between 1 and {domain.get_max_apart_nr()}!")

    apartment = find_apartment_by_nr(apartments, apartment_nr)

    if apartment is not None:
        domain.set_all_expenses(apartment, 0)

    else:
        raise ValueError(f"Apartment {apartment_nr} is not occupied. All of its expenses are already 0.")


def remove_all_type_expenses(apartments, expense_type):
    """
    Removes all <expense_type> type expenses from all apartments

    :param apartments: The list of apartments; list of dictionaries
    :param expense_type: The type of expense we want to remove from all apartments
    """
    check_available_expense(expense_type)  # Checks to see if the expense is available
    check_not_total(expense_type)

    for apartment in apartments:
        domain.set_any_expense(apartment, expense_type, 0)


def replace_expense(apartments, apart_nr, expense_type, expense_amount):
    """
    Replaces the expense for the <expense_type> expense of the <apart_nr> apartment with a new expense value.

    :param apartments: The list of apartments; list of dictionaries
    :param apart_nr: The number of the apartment whose expense we want to change
    :param expense_type: The expense type we want to replace
    :param expense_amount: The new value to give to the expense

    :raise ValueError: if trying to replace expense of unoccupied apartment; if expense amount negative; if
    apartment number negative or greater than the maximum accepted apartment number 'max_apart'
    :raise KeyError: if given unavailable expense type
    """
    max_apart = domain.get_max_apart_nr()

    apartment = find_apartment_by_nr(apartments, apart_nr)
    if apartment is None:
        raise ValueError("This apartment is not occupied. There are no expenses to replace.")
    if expense_amount < 0:
        raise ValueError("The expense amount must be a positive integer.")
    if apart_nr <= 0 or apart_nr >= max_apart:
        raise ValueError(f"The apartment number must be a positive integer smaller than {max_apart}.")

    check_available_expense(expense_type)
    check_not_total(expense_type)

    domain.set_any_expense(apartment, expense_type, expense_amount)
    return "Changed apartment's {} {} expense to {}".format(apart_nr, expense_type, expense_amount)


def get_expense_type_for_all_apartments(apartments, expense_type):
    """
    Returns all of the expenses of a certain type for all apartments, along with the corresponding apartment numbers

    :param apartments: The list of apartments; list of dictionaries
    :param expense_type: The type of expense we want to find; string
    :return: list of tuples in format (<apartment_number>, <expense>) representing the expenses of
    type <expense_type>, sorted by <apartment_number>
    """
    available_expenses = domain.get_available_expenses()
    if expense_type not in available_expenses + ['total']:
        raise KeyError(f"The expense '{expense_type}' is not currently available.")

    expenses = [domain.get_any_expense(apart, expense_type) for apart in apartments]
    apart_nrs = [domain.get_apart_nr(apart) for apart in apartments]

    sorted_nrs_and_exps = sorted(zip(apart_nrs, expenses), key=lambda pair: pair[0])

    return sorted_nrs_and_exps


def sum_expense_type(apartments, expense_type):
    """
    Returns the total amount for the expenses of type <expense_type>

    :param apartments: The list of apartments; list of dictionaries
    :param expense_type: The type of the expense whose sum we want to find; string
    :return: The total amount of the expenses of type <expense_type>; positive integer
    """
    sorted_nrs_and_exps = get_expense_type_for_all_apartments(apartments, expense_type)
    values_sorted_nrs_and_exps = [expense[1] for expense in sorted_nrs_and_exps]
    return sum(values_sorted_nrs_and_exps)


def sorted_ascending_apartments_totals(apartments):
    """
    Returns a list of tuples of apartments in the format (<apartment_nr>, <total_expense>). This list will be in
    ascending order, according to the total amount of expenses

    :param apartments: The list of apartments; list of dictionaries
    :return: The list of tuples with the apartments in ascending order by the total expenses
    """
    sorted_by_ap_nr = get_expense_type_for_all_apartments(apartments, 'total')
    # Above command returns the list sorted by apartment number, we need sort by total expense

    return sorted(sorted_by_ap_nr, key=lambda tup: tup[1])


def sorted_expense_types(apartments):
    """
    Returns a list of tuples of expenses in the format (<expense_type>, <total_of_expense_type>). Each element will
    be the sum of that expense type across all apartments. This list will be in ascending order, sorted by
    the amount of money. Note: The 'total' expense will not be in this list. It would obviously always be the
    first element in the list.

    :param apartments: The list of apartments; list of dictionaries
    :return: The list of tuples with the expenses in ascending order by their amounts
    """
    available_expenses = domain.get_available_expenses()
    expense_totals_across_apartments = [sum_expense_type(apartments, expense) for expense in available_expenses]

    return sorted(zip(available_expenses, expense_totals_across_apartments), key=lambda tup: tup[1])


def get_expenses_one_apartment(apartments, apartment_nr):
    """
    Returns all the expenses of the apartment with apartment number <apart_nr> (including total expense)

    :param apartments: The list of apartments; list of dictionaries
    :param apartment_nr: The number of the apartment whose expenses we want to return
    :return: A list of tuples containing all the expenses, including total expense. The format of every
    element in the list returned is (<expense_type>, <expense_amount>); as types that is (<string>, <positive int>)
    :raise ValueError: if the input apartment number is negative or greater than the maximum accepted apartment
    number; if the apartment <apartment_nr> is not occupied, so there are no expenses (by default)
    """
    max_apartments = domain.get_max_apart_nr()
    available_expenses = domain.get_available_expenses()

    if apartment_nr <= 0 or apartment_nr > max_apartments:
        raise ValueError(f"The apartment number must be a positive integer in the interval [0, {max_apartments}].")

    apartment = find_apartment_by_nr(apartments, apartment_nr)
    if apartment is None:
        raise ValueError(f"Apartment {apartment_nr} is not occupied.\n"
                         f"Expenses {', '.join([expense.title() for expense in available_expenses + ['total']])}"
                         f" are all equal to 0.")

    # Important note: the command 'available_expenses + ['total']' actually creates a new list and this new list
    # is used within this function. The original list of available expenses is NOT modified, which is actually
    # what we want, we don't want to add 'total' to the list of available expenses, since we decided to
    # implement the apartment object design in this manner

    # Get the expenses as a list of tuples
    expenses_of_apart = list(domain.get_all_expenses_of_apart(apartment).items())
    total_expenses = domain.get_apart_total_exp(apartment)
    expenses_of_apart = expenses_of_apart + [('total', total_expenses)]  # Add the total expense to the list

    return expenses_of_apart


def max_apartment_expense(apartments, apart_nr):
    """
    Returns the maximum expense type of an apartment, along with the value of this expense.

    :param apartments: The list of apartments; list of dictionaries
    :param apart_nr: The apartment number whose maximum expense should be returned; positive integer
    :return: A tuple in the format (<expense_type>, <expense_value>) having the name and value of the maximum
    expense type of an apartment; tuple of (string, positive integer)
    """
    expenses_of_apartment = get_expenses_one_apartment(apartments, apart_nr)
    expenses_of_apartment.pop()  # Remove the total expenses, this would always be the maximum
    return max(expenses_of_apartment, key=lambda tup: tup[1])


def get_totals_with_condition(apartments, comparison_sign, expense_amount):
    """
    Finds all the total expenses that satisfy a condition given by the comparison sign

    :param apartments: The list of apartments; list of dictionaries
    :param comparison_sign: The comparison sign; string
    :param expense_amount: The expense amount that will be used in the condition
    :return: A list of tuples, where the first element is the apartment number and the second element
    is the total expense of that apartment, which will satisfy the given condition
    :raise ValueError: if <comparison_sign> is not accepted; if <expense_amount> is negative
    """
    if comparison_sign not in ['<', '=', '>']:
        raise ValueError("This comparison is not available yet.")
    if expense_amount < 0:
        raise ValueError("Expense amounts should be positive integers!")

    total_expenses = [domain.get_apart_total_exp(apart) for apart in apartments]
    all_numbers = [domain.get_apart_nr(apart) for apart in apartments]

    comparison_dict = {'>': lambda a, b: a > b, '=': lambda a, b: a == b, '<': lambda a, b: a < b}

    filtered_apartments = [(number, total) for number, total in zip(all_numbers, total_expenses) if
                           comparison_dict[comparison_sign](total, expense_amount)]
    sorted_filtered_apartments = sorted(filtered_apartments, key=lambda tup: tup[0])

    return sorted_filtered_apartments


def filter_by_expense_type(apartments, expense_type):
    """
    Removes all expenses from all apartments, with the exception of the expense type given by the argument
    <expense_type>. This function has a filtering effect.

    :param apartments: The list of apartments; list of dictionaries
    :param expense_type: The expense type that dictates which expenses are to be kept; string
    """
    check_available_expense(expense_type)

    # We need to copy the list so we don't change it, removing <expense_type> from the original list
    available_expenses = domain.get_available_expenses()
    expenses_to_remove = [expense for expense in available_expenses if expense != expense_type]

    for expense_type in expenses_to_remove:
        remove_all_type_expenses(apartments, expense_type)


def filter_by_value(apartments, value):
    """
    Removes all expenses which have a value greater than or equal to <value>.
    This function has a filtering effect.

    :param apartments: The list of apartments; list of dictionaries
    :param value: The value against which the function compares the expenses; positive integer
    :return: -
    :raise ValueError: if <value> given by user is negative
    """
    available_expenses = domain.get_available_expenses()
    if value < 0:
        raise ValueError("The filtering value cannot be negative.")

    for apartment in apartments:
        for expense_type in available_expenses:
            if domain.get_any_expense(apartment, expense_type) >= value:
                domain.set_any_expense(apartment, expense_type, 0)


def check_state_change(apartments, states, current_state):
    """
    Checks if the state of the data has changed. If the state has changed, the previous state will be added
    in the list of states, so that we have access to this previous state in the future, if we will ever need it.
    The last state will be returned, regardless of whether or not the state has changed

    :param apartments: The list of apartments; list of dictionaries
    :param states: The list of states throughout the program's life; list of lists of dictionaries
    :param current_state: The current state of the data, has to be aligned with <apartments>; list of dictionaries
    :return: The last state; list of dictionaries
    """

    if apartments != current_state:
        states.append(current_state)
        current_state = deepcopy(apartments)

    return current_state


# noinspection PyUnusedLocal
def undo(apartments, states, current_state):
    """
    Restores the state of the data to its form before the last command. If there is no last command, this function
    does nothing.

    :param apartments: The list of apartments; list of dictionaries
    :param states: The previous states of the data, which have been saved through the lifetime of the program;
    the datatype of <states> is list of lists of dictionaries
    :param current_state: The current state of the data before the previous command; this parameter is a helper in
    recording the state changes during the program's execution. It has to be changed during the undo()
    function in order to be aligned with the <apartments> parameter; list of dictionaries
    :return:
    """

    if len(states) == 0:
        raise ValueError("You cannot use the undo command anymore!\n"
                         "The program has the state it had at the beginning.")

    apartments = states.pop()
    current_state = deepcopy(apartments)
    return apartments, current_state
