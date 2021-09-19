import traceback
from random import sample, randint


# ---------------------------------------------------------------------- #
# ------------------------------- DOMAIN ------------------------------- #
# ---------------------------------------------------------------------- #


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
    Returns the currently available expense types as a list of strings
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


def update_total_expenses(apartment):
    """
    Updates the apartment's total expenses

    :param apartment: The apartment whose total expenses we want to update; dictionary
    """
    expenses_sum = sum(apartment['expenses'].values())
    set_apart_total_exp(apartment, expenses_sum)


# ----------------------------------------------------------------------- #
# ------------------------------ FUNCTIONS ------------------------------ #
# ----------------------------------------------------------------------- #


def find_apartment_by_nr(apartments, apart_nr):
    """
    Checks to see if the 'apart_nr' apartment number is currently occupied. If it is, the function returns this
    apartment

    :param apartments: The list of apartments; list of dictionaries
    :param apart_nr: The number of the apartment to search for; positive integer
    :return: The apartment from the list of apartments that 'apart_nr' occupies IF found (in this case, returns dict);
    Returns None if 'apart_nr' not occupied
    """
    res = list(filter(lambda x: get_apart_nr(x) == apart_nr, apartments))
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

    max_apart_nr = get_max_apart_nr()
    if apart_nr > max_apart_nr:
        raise ValueError("We don't have that many apartments! Maximum is {}.".format(max_apart_nr))

    if find_apartment_by_nr(apartments, apart_nr) is not None:
        raise ValueError("This apartment is occupied! Try a different apartment number.")

    new_apartment = create_apartment(apart_nr)
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

    max_apart_nr = get_max_apart_nr()
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

    max_apart_nr = get_max_apart_nr()
    available_expense_types = get_available_expenses()
    apart_nrs = sample(range(1, max_apart_nr + 1), nr_of_apartments)

    for apart_nr in apart_nrs:
        new_apartment = occupy_new_apartment(apartments, apart_nr)
        for exp_type in available_expense_types:
            new_exp = randint(exp_lb, exp_ub)
            set_any_expense(new_apartment, exp_type, new_exp)


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
    args = [arg for arg in args if arg not in ['to', 'with', 'the', 'so', '', 'apartment']]

    return cmd, args


def parse_1_args(args):
    """
    Parses the arguments in the case of a command that can have just one argument

    :param args: The argument as a string in a list (e.g., ['25'], or ['water'])
    :return: The parsed argument in a list. It can now be used by the program (e.g., [25], or ['water']); list
    :raise ValueError: if given float numbers
    :raise KeyError: if given garbage as expense
    """

    available_expenses = get_available_expenses()

    err_msg = "The apartment number must be a positive integer!"
    try:
        args[0] = int(args[0])
    except ValueError:
        if any(char.isdigit() for char in args[0]):
            raise ValueError(err_msg)
        elif args[0] not in available_expenses:
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
    available_expenses = get_available_expenses()
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

    if expense_type not in get_available_expenses():
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

    current_exp_amount = get_any_expense(apart_to_add_to, expense_type)
    new_expense_amount = current_exp_amount + expense_amount
    set_any_expense(apart_to_add_to, expense_type, new_expense_amount)


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
    max_apartments = get_max_apart_nr()

    if start_ap_nr > end_ap_nr:
        start_ap_nr, end_ap_nr = end_ap_nr, start_ap_nr  # Swap the order if not already increasing

    if (start_ap_nr <= 0 and end_ap_nr <= 0) or (start_ap_nr > max_apartments and end_ap_nr > max_apartments):
        raise ValueError("Please input apartment numbers between 1 and {}.".format(max_apartments))

    start_ap_nr = max(1, start_ap_nr)
    end_ap_nr = min(200, end_ap_nr)

    for apart_nr in range(start_ap_nr, end_ap_nr + 1):
        apartment = find_apartment_by_nr(apartments, apart_nr)

        if apartment is not None:
            set_all_expenses(apartment, 0)

    return start_ap_nr, end_ap_nr


def remove_all_expenses_from_apartment(apartments, apartment_nr):
    """
    Removes all expenses from the apartment with apartment number <apartment_nr>

    :param apartments: The list of apartments; list of dictionaries
    :param apartment_nr: The apartment number whose expenses we want to remove
    """
    if apartment_nr <= 0 or apartment_nr > get_max_apart_nr():
        raise ValueError(f"Apartment numbers must be positive integers between 1 and {get_max_apart_nr()}!")

    apartment = find_apartment_by_nr(apartments, apartment_nr)

    if apartment is not None:
        set_all_expenses(apartment, 0)

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
        set_any_expense(apartment, expense_type, 0)


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
    max_apart = get_max_apart_nr()

    apartment = find_apartment_by_nr(apartments, apart_nr)
    if apartment is None:
        raise ValueError("This apartment is not occupied. There are no expenses to replace.")
    if expense_amount < 0:
        raise ValueError("The expense amount must be a positive integer.")
    if apart_nr <= 0 or apart_nr >= max_apart:
        raise ValueError(f"The apartment number must be a positive integer smaller than {max_apart}.")

    check_available_expense(expense_type)
    check_not_total(expense_type)

    set_any_expense(apartment, expense_type, expense_amount)
    return "Changed apartment's {} {} expense to {}".format(apart_nr, expense_type, expense_amount)


def get_expense_type_for_all_apartments(apartments, expense_type):
    """
    Returns all of the expenses of a certain type for all apartments, along with the corresponding apartment number

    :param apartments: The list of apartments; list of dictionaries
    :param expense_type: The type of expense we want to find; string
    :return: list of tuples in format (<apartment_number>, <expense>) representing the expenses of
    type <expense_type>, sorted by <apartment_number>
    """
    available_expenses = get_available_expenses()
    if expense_type not in available_expenses:
        raise KeyError(f"The expense '{expense_type}' is not currently available.")

    expenses = [get_any_expense(apart, expense_type) for apart in apartments]
    apart_nrs = [get_apart_nr(apart) for apart in apartments]

    sorted_nrs_and_exps = sorted(zip(apart_nrs, expenses), key=lambda pair: pair[0])

    return sorted_nrs_and_exps


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
    max_apartments = get_max_apart_nr()
    available_expenses = get_available_expenses()

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

    expenses_of_apart = list(get_all_expenses_of_apart(apartment).items())  # Get the expenses as a list of tuples
    total_expenses = get_apart_total_exp(apartment)
    expenses_of_apart = expenses_of_apart + [('total', total_expenses)]  # Add the total expense to the list

    return expenses_of_apart


def get_totals_with_condition(apartments, comparison_sign, expense_amount):
    """
    Finds all the total expenses that satisfy a condition given by the comparison sign

    :param apartments: The list of apartments; list of dictionaries
    :param comparison_sign: The comparison sign; string
    :param expense_amount: The expense amount that will be used in the condition
    :return: A list of tuples, where the first element is the apartment number and the second element
    is the total expense of that apartment, which will satisfy the given condition
    """
    if comparison_sign not in ['<', '=', '>']:
        raise ValueError("This comparison is not available yet.")
    if expense_amount < 0:
        raise ValueError("Expense amounts should be positive integers!")

    total_expenses = [get_apart_total_exp(apart) for apart in apartments]
    all_numbers = [get_apart_nr(apart) for apart in apartments]

    comparison_dict = {'>': lambda a, b: a > b, '=': lambda a, b: a == b, '<': lambda a, b: a < b}

    filtered_apartments = [(number, total) for number, total in zip(all_numbers, total_expenses) if
                           comparison_dict[comparison_sign](total, expense_amount)]
    sorted_filtered_apartments = sorted(filtered_apartments, key=lambda tup: tup[0])

    return sorted_filtered_apartments


# ------------------------------------------------------------------ #
# ------------------------------- UI ------------------------------- #
# ------------------------------------------------------------------ #


def ui_print_all_options():
    """
    Prints the available options to the user
    """

    print("These are the currently available commands:\n"
          "\t1) add <apartment> <type> <amount> - Add an expense of <amount> RON and <type> type to apartment"
          "<apartment>\n"
          "\t2) remove <apartment> - Remove all expenses for apartment <apartment>\n"
          "\t3) remove <start apartment> to <end apartment> - Remove all expenses for apartments <start apartment>"
          "to4) <end apartment>\n"
          "\t5) remove <type> - Remove all expenses of type <type> for all apartments.\n"
          "\t6) replace <apartment> <type> with <amount> - Replace the amount of the expense with type <type> for"
          "apartment <apartment> with with <amount>\n"
          "\t7) list - Display all expenses\n"
          "\t8) list <apartment> - Display all expenses for apartment <apartment>\n"
          "\t9) list [ < | = | > ] <amount> - Display all apartments having total expenses <, =, or > amount <amount>\n"
          "\t10) occupy <apartment> - Occupy apartment <apartment> if it is not already occupied\n"
          "\t11) clear <apartment> - Clear apartment <apartment> if it is occupied, removing it from the list\n"
          "\t12) print - Print all occupied apartments. Use this if you want to see which apartments are available\n"
          "\t13) exit - Stop the program")


def ui_occupy_apartment(apartments, apart_nr):
    """
    Occupies an apartment (if it is not already occupied) and initialises its expenses (by default to 0)

    :param apartments: The current list of apartments; list of dictionaries
    :param apart_nr: The number of the apartment that the client wants to occupy; positive integer
    """
    occupy_new_apartment(apartments, apart_nr)  # raises ValueError if 'apart_nr' occupied
    print("Apartment number {} is now occupied. All of this apartment's expenses have been set at 0.".format(apart_nr))


def ui_clear_apartment(apartments, apart_nr):
    """
    Clears an apartment (if it is occupied). If this command is applied, the apartment will be removed from
    the list of apartments. Note: This is different than the 'remove' command applied on an apartment, as that
    command will set an apartment's expenses to 0, but the apartment will be kept on the list of occupied apartments.

    :param apartments: The list of apartments; list of dictionaries
    :param apart_nr: The number of the apartment which we want to remove; positive integer
    """
    clear_apartment(apartments, apart_nr)
    print(f"Apartment {apart_nr} has been removed from the list of apartments!")


def ui_clear_range_of_apartments(apartments, start_apart_nr, end_apart_nr):
    """
    Clears a range of apartments (or at least the apartments that are occupied from the given range)

    :param apartments: The list of apartments; list of dictionaries
    :param start_apart_nr: The lower bound of the range of apartments to be cleared; positive integer
    :param end_apart_nr: The upper bound of the range of apartments to be cleared; positive integer
    """
    clear_range_of_apartments(apartments, start_apart_nr, end_apart_nr)
    print(f"All apartments from apartment {start_apart_nr} to apartment {end_apart_nr} have been cleared.")


def print_all_occupied_apartments(apartments):
    """
    Displays on the numbers of the apartments that are already occupied

    :param apartments: The list of apartments; list of dictionaries
    :raise ValueError: if there are no occupied apartments
    """
    if len(apartments) == 0:
        raise ValueError("There are no occupied apartments! All expenses of all apartments are 0.")

    occupied = list(map(get_apart_nr, apartments))
    occupied = sorted(occupied)
    print("These apartments are occupied:")
    for index, apart in enumerate(occupied):
        print("\t{}) Apartment number {}".format(index + 1, apart))


def ui_print_prompt(msg):
    """
    Prompt that keeps running until the answer given by the user is either yes ('y', 'Y', 'yes', 'yES', etc)
    or no('N', 'no', etc)
    """
    while True:
        answer = input(msg)
        try:
            answer = answer.strip().lower()
            if answer in ['y', 'yes']:
                return True
            elif answer in ['n', 'no']:
                return False
            else:
                raise ValueError
        except Exception as err:
            print(str(type(err)) + ": Please answer with Y(yes) or N(no).")


def ui_add_expense(apartments, args):
    """
    Adds a new expense to an apartment

    :param apartments: The list of apartments; list of dictionaries
    :param args: Arguments for the 'add' command in the format [<apartment_nr>, <exp_type>, <exp_amount>]; list
    """

    apart_nr, expense_type, expense_amount = args
    try:
        add_expense(apartments, apart_nr, expense_type, expense_amount)

    except ValueError as ve:
        if str(ve) == "This apartment is not occupied.":
            user_answer = ui_add_expense_prompt()
            if user_answer:
                add_expense(apartments, apart_nr, expense_type, expense_amount, talked_to_user=True)
                print(f"Apartment number {apart_nr} is now occupied and an expense of {expense_amount} has been added "
                      f"to its {expense_type} expense.")
            else:
                print("No action was taken.")

        else:
            raise ve

    else:
        print(f"Added {expense_amount} RON to apartment's {apart_nr} '{expense_type}' expense.")


def ui_add_expense_prompt():
    """
    In the case of an 'add' command on an apartment that is not currently occupied, this function is used
    to display a prompt on the screen asking if he/she wants to occupy the apartment and add that expense to it.
    In case the answer of the user is negative, nothing happens as the apartment is not occupied.
    """
    msg = "This apartment is not occupied. Do you want to occupy it and add the expense to the newly" \
          " occupied apartment?(Y/N) "
    return ui_print_prompt(msg)


def ui_clear_apartment_prompt():
    """
    Asks the user if he/she wants to clear the apartment, i.e., remove the apartment from the list
    :return: True if the apartment should be cleared; False otherwise
    """
    msg = "Do you want to clear the apartment(s)\n(Careful: This will remove the apartment(s) from " \
          "the list of occupied apartments)?\n(Y/N) "
    return ui_print_prompt(msg)


def ui_remove_expense(apartments, args):
    """
    Removes expenses. What this function can do: remove all expenses for an apartment, remove all expenses for
    a range of apartments, or remove all expenses of a certain type for all apartments

    :param apartments: The list of apartments; list of dictionaries
    :param args: The arguments of the 'remove' command in one of the accepted formats ([<apartment>],
    [<start_apartment>, <end_apartment>], or [<type>]); list of integers or list of a string

    :raise ValueError: if apartment numbers given are not in the range [0, <max_apartment_number>]
    :raise TypeError: if too many/too few arguments are provided
    """
    if len(args) == 2:
        start, end = args
        start, end = remove_all_from_to(apartments, start, end)
        print(f"All expenses from all apartments from apartment {start} to apartment {end} have been removed.")
        if ui_clear_apartment_prompt():
            ui_clear_range_of_apartments(apartments, start, end)
        else:
            print("The apartments weren't removed from the list of apartments.")

    elif len(args) == 1 and isinstance(args[0], int):
        remove_all_expenses_from_apartment(apartments, args[0])
        print(f"All expenses from apartment {args[0]} have been removed.")
        if ui_clear_apartment_prompt():
            ui_clear_apartment(apartments, args[0])
        else:
            print("The apartment wasn't removed from the list of apartments.")

    elif len(args) == 1 and isinstance(args[0], str):
        remove_all_type_expenses(apartments, args[0])
        print(f"All {args[0]} expense types from all apartments have been removed.")

    else:
        raise TypeError("The 'remove' command can accept one or two arguments!")


def ui_replace_expense(apartments, args):
    """
    Replaces the expense of a certain apartment (for a given <expense_type>) with a new expense

    :param apartments: The list of apartments; list of dictionaries
    :param args: The arguments (given by the user) for the 'remove' command; list
    """

    apart_nr, expense_type, expense_amount = args
    replace_msg = replace_expense(apartments, apart_nr, expense_type, expense_amount)
    print(replace_msg)


def ui_list_all(apartments):
    """
    Displays on the screen all expenses for all apartments

    :param apartments: The list of apartments; list of dictionaries
    """
    available_expenses = get_available_expenses()

    for expense_type in available_expenses + ['total']:
        sorted_nrs_and_exps = get_expense_type_for_all_apartments(apartments, expense_type)

        print(f"These are all the {expense_type.title()} expenses:")
        for index, (nr, exp) in enumerate(sorted_nrs_and_exps):
            print("\t{}) Apartment {} - {} RON".format(index + 1, nr, exp))

        print()


def ui_list_one_apartment(apartments, apartment_nr):
    """
    Displays on the screen all expenses of an apartment (including total expense)

    :param apartments: The list of apartments; list of dictionaries
    :param apartment_nr: The number of the apartment whose expenses we want to print; positive integer
    """
    list_of_expenses = get_expenses_one_apartment(apartments, apartment_nr)

    print(f"These are apartment's {apartment_nr} expenses:")
    for expense_type, expense_amount in list_of_expenses:
        print(f"\t{expense_type.title()} - {expense_amount} RON")


def ui_list_with_comparison(apartments, comparison_sign, expense_amount):
    """
    Displays on the screen all apartments whose total expenses satisfy a criterion, where the available
    criteria are: '<', '>' (the strict inequalities), and '=' (equality)

    :param apartments: The list of apartments; list of dictionaries
    :param comparison_sign: The comparison sign; string
    :param expense_amount: The number which controls the inequalities/equality; positive integer
    :raise ValueError: if garbage given instead of a proper comparison sign; if expense amount given negative
    """
    sorted_filtered_apartments = get_totals_with_condition(apartments, comparison_sign, expense_amount)

    print("These are all the apartments whose total expenses are {} {} RON:".format(comparison_sign, expense_amount))
    for index, (apart_nr, total_exp) in enumerate(sorted_filtered_apartments):
        print("\t{}) Apartment number {} - Total = {} RON".format(index + 1, apart_nr, total_exp))


def ui_list_expenses(apartments, args):
    """
    Handles all the displaying functions, which will be called according to the 'args' argument

    :param apartments: The list of apartments; list of dictionaries
    :param args: The arguments (given by the user) for the 'list' command; list
    :raise TypeError: if too many arguments given to the 'list' command
    """

    if len(args) == 0:
        ui_list_all(apartments)

    elif len(args) == 1:
        apart_nr = args[0]
        ui_list_one_apartment(apartments, apart_nr)

    elif len(args) == 2:
        comparison_sign, expense_amount = args[0], args[1]
        ui_list_with_comparison(apartments, comparison_sign, expense_amount)
    else:
        raise TypeError("Too many arguments given to the command!")


def helper_run_menu_cmd(apartments, commands, cmd, args):
    """
    Returns all the arguments that we have to pass for the current command. This function makes it possible
    to avoid a long if/elif/else block in the main function

    :param apartments: The list of apartments; list of dictionaries
    :param commands: The available commands; dictionary
    :param cmd: The parsed command that the program has to execute (e.g., 'add', 'remove', 'list', etc)
    :param args: The parsed list of arguments given by the user (e.g., [15, 'water', 200])

    :return: The necessary arguments for the command as a list
    """
    if cmd == 'info':
        return []
    elif cmd == 'print':
        return [apartments]
    elif cmd == 'occupy' or cmd == 'clear':
        try:
            return apartments, args[0]
        except IndexError:
            raise IndexError("The 'occupy' and 'clear' functions expect a parameter!")
    elif cmd in commands.keys():
        return apartments, args


def run_menu_cmd():
    """
    Handles the command based main menu

    :return: Returns when the user stops the execution/when an unknown error occurs
    """

    apartments = []
    commands = {'add': ui_add_expense, 'remove': ui_remove_expense, 'replace': ui_replace_expense,
                'list': ui_list_expenses, 'info': ui_print_all_options, 'print': print_all_occupied_apartments,
                'occupy': ui_occupy_apartment, 'clear': ui_clear_apartment}

    fill_random_apartments(apartments)

    while True:
        try:
            cmd_line = input("Please enter your command\n"
                             "(Enter 'info' if you want to see all available commands)\n")
            # First, parse the cmd_line into something like ('add', [15, 'water', 200])
            cmd, args = parse_command_and_arguments(cmd_line)

            # print(cmd, args)

            # Then, get all the needed arguments for all possible cases into just one variable than we unpack
            # when calling functions. This is done in order to avoid a long if/elif/else block
            args = helper_run_menu_cmd(apartments, commands, cmd, args)

            if cmd == 'exit':
                return

            if cmd in commands.keys():
                commands[cmd](*args)

            else:
                print("Invalid command! Try again.")

        except (ValueError, TypeError, IndexError) as err:
            print(str(err))
        # KeyError automatically adds quotation marks, so we treat it separately, ignoring the first and last elements
        except KeyError as ke:
            print(str(ke)[1:-1])

        print()


# --------------------------------------------------------------------- #
# ------------------------------- TESTS ------------------------------- #
# --------------------------------------------------------------------- #


def set_up_test():
    """
    'Sets the stage' for the testing phase. Call this fn at the beginning of each testing fn

    :return students: A dummy variable; List of students made just for testing purposes
    """
    apartments = []
    new_apart = occupy_new_apartment(apartments, 1)
    set_apart_water_exp(new_apart, 100)
    set_apart_heating_exp(new_apart, 200)
    set_apart_gas_exp(new_apart, 300)
    set_apart_electricity_exp(new_apart, 400)
    set_apart_other_exp(new_apart, 500)

    new_apart = occupy_new_apartment(apartments, 2)
    set_apart_water_exp(new_apart, 50)
    set_apart_heating_exp(new_apart, 75)
    set_apart_gas_exp(new_apart, 100)
    set_apart_electricity_exp(new_apart, 30)
    set_apart_other_exp(new_apart, 40)

    new_apart = occupy_new_apartment(apartments, 3)
    set_apart_water_exp(new_apart, 10)
    set_apart_heating_exp(new_apart, 70)
    set_apart_gas_exp(new_apart, 90)
    set_apart_electricity_exp(new_apart, 80)
    set_apart_other_exp(new_apart, 20)

    return apartments


def test_parse_command():
    assert parse_command_and_arguments("Add    17,  WATER,  250 RON.") == ("add", [17, "water", 250])
    assert parse_command_and_arguments("Remove     25.") == ("remove", [25])
    assert parse_command_and_arguments("   Remove 5    to  17.") == ("remove", [5, 17])
    assert parse_command_and_arguments("Remove   THE   HEATING") == ("remove", ["heating"])
    assert parse_command_and_arguments("   Replace 25  water with    200  RON") == ("replace", [25, "water", 200])
    assert parse_command_and_arguments(" list     ") == ("list", [])
    assert parse_command_and_arguments(" LIST    32") == ("list", [32])
    assert parse_command_and_arguments("list   <     200") == ("list", ["<", 200])
    assert parse_command_and_arguments("EXIT  ") == ("exit", [])

    try:
        parse_command_and_arguments("Add -20 water")
        assert False
    except ValueError:  # Cannot have negative numbers => ValueError
        assert True

    try:
        parse_command_and_arguments("Remove   THE   phone")   # No expense called 'phone' => KeyError
        assert False
    except KeyError:
        assert True


def test_find_apartment_by_nr():
    apartments = set_up_test()
    assert (find_apartment_by_nr(apartments, 1) is not None) and \
           (find_apartment_by_nr(apartments, 2) is not None) and \
           (find_apartment_by_nr(apartments, 3) is not None)

    assert find_apartment_by_nr(apartments, 5) is None


def test_occupy_new_apartment():
    apartments = set_up_test()
    assert len(apartments) == 3
    occupy_new_apartment(apartments, 4)
    assert len(apartments) == 4

    try:
        occupy_new_apartment(apartments, -1)
        assert False
    except ValueError:
        assert True

    try:
        occupy_new_apartment(apartments, get_max_apart_nr() + 5)
        assert False
    except ValueError:
        assert True

    try:
        occupy_new_apartment(apartments, 2)
        assert False
    except ValueError:
        assert True


def test_clear_apartment():
    apartments = set_up_test()

    clear_apartment(apartments, 1)
    clear_apartment(apartments, 2)

    assert len(apartments) == 1

    try:
        clear_apartment(apartments, -1)
        assert False
    except ValueError:
        assert True

    try:
        clear_apartment(apartments, get_max_apart_nr() + 2)
        assert False
    except ValueError:
        assert True

    try:
        clear_apartment(apartments, 5)
        assert False
    except ValueError:
        assert True


def test_add_expense():
    apartments = set_up_test()
    add_expense(apartments, 1, 'water', 100)
    assert get_apart_water_exp(apartments[0]) == 200
    assert get_apart_total_exp(apartments[0]) == 1600

    try:
        add_expense(apartments, 2, 'total', 50)
        assert False
    except KeyError:
        assert True

    try:
        add_expense(apartments, 2, 'phone', 100)
        assert False
    except KeyError:
        assert True

    try:
        add_expense(apartments, 1, 'gas', -50)
        assert False
    except ValueError:
        assert True

    try:
        add_expense(apartments, 5, 'water', 100)
        assert False
    except ValueError:
        assert True

    add_expense(apartments, 5, 'water', 100, talked_to_user=True)
    assert len(apartments) == 4


def test_remove_all_from_to():
    apartments = set_up_test()

    remove_all_from_to(apartments, 1, 2)
    assert get_apart_total_exp(apartments[0]) == get_apart_total_exp(apartments[1]) == 0

    try:
        remove_all_from_to(apartments, 205, 210)
        assert False
    except ValueError:
        assert True

    try:
        remove_all_from_to(apartments, -10, -5)
        assert False
    except ValueError:
        assert True


def test_remove_all_expenses_from_apartment():
    apartments = set_up_test()
    try:
        remove_all_expenses_from_apartment(apartments, 5)
        assert False
    except ValueError:
        assert True

    try:
        remove_all_expenses_from_apartment(apartments, -5)
        assert False
    except ValueError:
        assert True

    try:
        remove_all_expenses_from_apartment(apartments, get_max_apart_nr() + 5)
        assert False
    except ValueError:
        assert True

    remove_all_expenses_from_apartment(apartments, 1)
    assert get_apart_total_exp(apartments[0]) == 0


def test_remove_all_type_expenses():
    apartments = set_up_test()
    try:
        remove_all_type_expenses(apartments, 'phone')
        assert False
    except KeyError:
        assert True

    try:
        remove_all_type_expenses(apartments, 'total')
        assert False
    except KeyError:
        assert True

    remove_all_type_expenses(apartments, 'gas')
    assert get_apart_gas_exp(apartments[0]) ==\
           get_apart_gas_exp(apartments[1]) ==\
           get_apart_gas_exp(apartments[2]) == 0

    # Check that the other expenses were not changed
    assert get_apart_water_exp(apartments[0]) != 0 and \
           get_apart_heating_exp(apartments[0]) != 0 and \
           get_apart_other_exp(apartments[0]) != 0 and \
           get_apart_electricity_exp(apartments[0]) != 0


def test_replace_expense():
    apartments = set_up_test()

    try:
        replace_expense(apartments, 5, 'gas', 200)
        assert False
    except ValueError:
        assert True

    try:
        replace_expense(apartments, 1, 'water', -100)
        assert False
    except ValueError:
        assert True

    try:
        replace_expense(apartments, get_max_apart_nr() + 5, 'water', 100)
        assert False
    except ValueError:
        assert True

    try:
        replace_expense(apartments, 1, 'phone', 500)
        assert False
    except KeyError:
        assert True

    try:
        replace_expense(apartments, 2, 'total', 100)
        assert False
    except KeyError:
        assert True

    replace_expense(apartments, 1, 'water', 0)
    assert get_apart_water_exp(apartments[0]) == 0
    assert get_apart_total_exp(apartments[0]) == 1400


def test_get_expense_type_for_all_apartments():
    apartments = set_up_test()
    assert get_expense_type_for_all_apartments(apartments, 'gas') == [(1, 300), (2, 100), (3, 90)]
    assert get_expense_type_for_all_apartments(apartments, 'water') == [(1, 100), (2, 50), (3, 10)]
    try:
        get_expense_type_for_all_apartments(apartments, 'phone')
        assert False
    except KeyError:
        assert True


def test_get_expenses_one_apartment():
    apartments = set_up_test()
    try:
        get_expenses_one_apartment(apartments, -1)
        assert False
    except ValueError:
        assert True

    try:
        get_expenses_one_apartment(apartments, get_max_apart_nr() + 5)
        assert False
    except ValueError:
        assert True

    try:
        get_expenses_one_apartment(apartments, 5)
        assert False
    except ValueError:
        assert True

    expenses_of_apart1 = get_expenses_one_apartment(apartments, 1)
    values_of_expenses_of_apart1 = [expense[1] for expense in expenses_of_apart1]

    # We also have to take into consideration that the total expense will also be returned in the list
    assert sorted(values_of_expenses_of_apart1) == [100, 200, 300, 400, 500, 1500]


def test_get_totals_with_condition():
    apartments = set_up_test()
    try:
        get_totals_with_condition(apartments, '>=', 100)
        assert False
    except ValueError:
        assert True

    try:
        get_totals_with_condition(apartments, '>', -100)
        assert False
    except ValueError:
        assert True

    sorted_filtered_apartments = get_totals_with_condition(apartments, '>', 280)
    values_sorted_filtered_apartments = [apart[1] for apart in sorted_filtered_apartments]
    assert values_sorted_filtered_apartments == [1500, 295]

    sorted_filtered_apartments = get_totals_with_condition(apartments, '<', 10)
    assert len(sorted_filtered_apartments) == 0


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


if __name__ == "__main__":
    run_all_tests()

    print("Hello!")

    try:
        run_menu_cmd()

    except Exception as ex:
        print("Unknown error caught: ", ex)
        traceback.print_exc()

    print("Have a great day!")
