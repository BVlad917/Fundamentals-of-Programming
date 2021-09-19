"""
The User Interface module. All print and input functions are handled here.
These functions call functions from the domain and functions module.
"""

from copy import deepcopy

import src.functions.functions as fns
from src.domain.entity import get_apart_nr, get_available_expenses


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
          "\t9) list [ < | = | > ] <amount> - Display all apartments having total expenses <, =, or > "
          "amount <amount>\n"
          "\t*10) sum <expense_type> - Display the total amount for the expenses having type <expense_type>\n"
          "\t*11) max <apartment> - Display the maximum expense type for apartment <apartment>\n"
          "\t*12) sort apartment - Display the list of apartments sorted ascending by total amount of expenses\n"
          "\t*13) sort type - Display the total amount of expenses for each type, sorted ascending by amount "
          "of money\n"
          "\t*14) filter <type> - Keep only the expenses for <type>\n"
          "\t*15) filter <value> - Keep only the expenses having an amount of money smaller than <value>\n"
          "\t*16) undo - the last operation that modified program data is reversed.\n"
          "\t17) occupy <apartment> - Occupy apartment <apartment> if it is not already occupied\n"
          "\t18) clear <apartment> - Clear apartment <apartment> if it is occupied, removing it from the list\n"
          "\t19) print - Print all occupied apartments. Use this if you want to see which apartments are available\n"
          "\t20) exit - Stop the program\n\n"
          "* - Added in Assignment 4")


def ui_occupy_apartment(apartments, apart_nr):
    """
    Occupies an apartment (if it is not already occupied) and initialises its expenses (by default to 0)

    :param apartments: The current list of apartments; list of dictionaries
    :param apart_nr: The number of the apartment that the client wants to occupy; positive integer
    """
    fns.occupy_new_apartment(apartments, apart_nr)  # raises ValueError if 'apart_nr' occupied
    print("Apartment number {} is now occupied. All of this apartment's expenses have been set at 0.".format(apart_nr))


def ui_clear_apartment(apartments, apart_nr):
    """
    Clears an apartment (if it is occupied). If this command is applied, the apartment will be removed from
    the list of apartments. Note: This is different than the 'remove' command applied on an apartment, as that
    command will set an apartment's expenses to 0, but the apartment will be kept on the list of occupied apartments.

    :param apartments: The list of apartments; list of dictionaries
    :param apart_nr: The number of the apartment which we want to remove; positive integer
    """
    fns.clear_apartment(apartments, apart_nr)
    print(f"Apartment {apart_nr} has been removed from the list of apartments!")


def ui_clear_range_of_apartments(apartments, start_apart_nr, end_apart_nr):
    """
    Clears a range of apartments (or at least the apartments that are occupied from the given range)

    :param apartments: The list of apartments; list of dictionaries
    :param start_apart_nr: The lower bound of the range of apartments to be cleared; positive integer
    :param end_apart_nr: The upper bound of the range of apartments to be cleared; positive integer
    """
    fns.clear_range_of_apartments(apartments, start_apart_nr, end_apart_nr)
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
        fns.add_expense(apartments, apart_nr, expense_type, expense_amount)

    except ValueError as ve:
        if str(ve) == "This apartment is not occupied.":
            user_answer = ui_add_expense_prompt()
            if user_answer:
                fns.add_expense(apartments, apart_nr, expense_type, expense_amount, talked_to_user=True)
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
        start, end = fns.remove_all_from_to(apartments, start, end)
        print(f"All expenses from all apartments from apartment {start} to apartment {end} have been removed.")
        if ui_clear_apartment_prompt():
            ui_clear_range_of_apartments(apartments, start, end)
        else:
            print("The apartments weren't removed from the list of apartments.")

    elif len(args) == 1 and isinstance(args[0], int):
        fns.remove_all_expenses_from_apartment(apartments, args[0])
        print(f"All expenses from apartment {args[0]} have been removed.")
        if ui_clear_apartment_prompt():
            ui_clear_apartment(apartments, args[0])
        else:
            print("The apartment wasn't removed from the list of apartments.")

    elif len(args) == 1 and isinstance(args[0], str):
        fns.remove_all_type_expenses(apartments, args[0])
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
    replace_msg = fns.replace_expense(apartments, apart_nr, expense_type, expense_amount)
    print(replace_msg)


def ui_list_all(apartments):
    """
    Displays on the screen all expenses for all apartments

    :param apartments: The list of apartments; list of dictionaries
    """
    available_expenses = get_available_expenses()

    for expense_type in available_expenses + ['total']:
        sorted_nrs_and_exps = fns.get_expense_type_for_all_apartments(apartments, expense_type)

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
    list_of_expenses = fns.get_expenses_one_apartment(apartments, apartment_nr)

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
    sorted_filtered_apartments = fns.get_totals_with_condition(apartments, comparison_sign, expense_amount)

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


def ui_sum_expense_type(apartments, expense_type):
    """
    Displays on the screen the total amount of the expenses of type <expense_type>

    :param apartments: The list of apartments; list of dictionaries
    :param expense_type: The expense type whose sum we want; string
    """
    sum_exp_type = fns.sum_expense_type(apartments, expense_type)
    print(f"The total amount for the expenses of type '{expense_type}' is {sum_exp_type}.")


def ui_sorted_apartments_by_total(apartments):
    """
    Displays on the screen the list of apartments in ascending order by their total expenses.

    :param apartments: The list of apartments; list of dictionaries
    """
    sorted_by_totals = fns.sorted_ascending_apartments_totals(apartments)
    print("These are the currently occupied apartments in ascending order by their total expenses:")
    for index, nr_and_totals in enumerate(sorted_by_totals):
        print(f"\t{index + 1}) Apartment {nr_and_totals[0]} - {nr_and_totals[1]} RON")


def ui_sorted_expense_types(apartments):
    """
    Displays on the screen the list of expenses in ascending order by their amount of money. I.e., each element that
    will be printed on the screen will be the sum of a certain expense type across all apartments.

    :param apartments: The list of apartments; list of dictionaries
    """
    expense_types_sorted = fns.sorted_expense_types(apartments)
    print("These are the total amount of expenses of each type, sorted in ascending order by their "
          "sum across apartments:")

    for index, expense_and_value in enumerate(expense_types_sorted):
        print(f"\t{index + 1}) {expense_and_value[0].title()} - {expense_and_value[1]} RON")


def ui_display_sorted(apartments, argument):
    """
    Handles all the 'display sorted' type of commands. In the case the argument is the string 'apartment',
    it displays the list of apartments in ascending order by their total expenses. In the case the argument
    is 'type' it displays the total amount of expenses for each type in ascending order by amount of money.

    :param apartments: The list of apartments; list of dictionaries
    :param argument: The argument that determined what the function has to display; string
    """
    accepted_args_to_fns = {'apartment': ui_sorted_apartments_by_total, 'type': ui_sorted_expense_types}

    if argument not in accepted_args_to_fns.keys():
        raise KeyError(f"The command 'sort' does not accept the argument '{argument}'.")

    accepted_args_to_fns[argument](apartments)


def ui_max_apartment_expense(apartments, apart_nr):
    """
    Displays on the screen the maximum expense type of an apartment, along with the value of this maximum
    expense type.

    :param apartments: The list of apartments; list of dictionaries
    :param apart_nr: The apartment number whose maximum expense should be displayed; positive integer
    """
    maximum_expense_type, maximum_expense_value = fns.max_apartment_expense(apartments, apart_nr)
    print(f"The maximum expense of apartment {apart_nr} is the expense of type '{maximum_expense_type.title()}' "
          f"with {maximum_expense_value} RON.")


def ui_filter_by_expense_type(apartments, expense_type):
    """
    Removes all expenses from all apartments except the expense type given by the argument <expense_type>.

    :param apartments: The list of apartments; list of dictionaries
    :param expense_type: The expense type which we want to keep. All other expenses will be removed,
    for all apartments
    """
    fns.filter_by_expense_type(apartments, expense_type)
    print(f"All expenses except the expense '{expense_type}' have been removed from all apartments.")


def ui_filter_by_value(apartments, value):
    """
    Filters the expenses, removing all expenses having a value greater than or equal to <value>. Thus, only the
    expenses having an expense value smaller than <value> will be kept.

    :param apartments: The list of apartments; list of dictionaries
    :param value: The value against which the expenses will be filtered
    """
    fns.filter_by_value(apartments, value)
    print(f"All expenses that are greater than or equal to {value} have been removed.")


def ui_filter(apartments, argument):
    """
    Handles the filtering functions. If the argument is an expense type (so a string), this function will call
    the function responsible for filtering by expense type, and all expenses except this expense type will be
    removed. If the argument is a value (so a positive integer), this function will call the function responsible
    for filtering by value, and only the expenses that are smaller than this value will be kept.

    :param apartments: The list of apartments; list of dictionaries
    :param argument: The argument of the filter function; either an integer or a string
    """
    if isinstance(argument, str):
        ui_filter_by_expense_type(apartments, argument)
    elif isinstance(argument, int):
        ui_filter_by_value(apartments, argument)
    else:
        raise ValueError("The filter function expects either a string or a positive integer as parameters.")


def ui_undo(apartments, states, current_state, commands_through_time):
    """
    Restores the program to its state before the last performed command. If the program is already at the
    initial state, nothing happens.

    :param apartments: The list of apartments; list of dictionaries
    :param states: The list of the states of data throughout the program's lifetime. The datatype of this
    variable is list of lists of dictionaries
    :param current_state: The current state. This variable also has to be changed during every undo such that it
    is aligned with the apartments variable (this necessary alignment stems from the fact that this variable
    is used in detecting when changes in the data have been performed, so that we can keep track of previous states);
    The datatype of <current_state> is list of dictionaries
    :param commands_through_time: The commands that were given by the user and in one way or another modified the
    state of the program's data. List of strings
    """
    apartments, current_state = fns.undo(apartments, states, current_state)
    last_command = commands_through_time.pop()
    print("Your last performed command:")
    print("\t'" + last_command + "'")
    print("Was undone.")
    return apartments, current_state


def helper_run_menu_cmd(apartments, commands, cmd, args):
    """
    Returns all the arguments that we have to pass for the current command. This function makes it possible
    to avoid a long if/elif/else block in the main function

    :param apartments: The list of apartments; list of dictionaries
    :param commands: The available commands; dictionary
    :param cmd: The parsed command that the program has to execute (e.g., 'add', 'remove', 'list', etc)
    :param args: The parsed list of arguments given by the user (e.g., [15, 'water', 200])
    states throughout the program's lifetime

    :return: The necessary arguments for the command as a list
    """
    if cmd in ['info']:
        return []
    elif cmd == 'print':
        return [apartments]
    elif cmd in ['occupy', 'clear', 'sum', 'sort', 'max', 'filter']:
        try:
            return apartments, args[0]
        except IndexError:
            raise IndexError("The given command expects a parameter!")
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
                'occupy': ui_occupy_apartment, 'clear': ui_clear_apartment, 'sum': ui_sum_expense_type,
                'sort': ui_display_sorted, 'max': ui_max_apartment_expense, 'filter': ui_filter}

    fns.fill_random_apartments(apartments)

    # We need a list that will keep track of all of our states throughout the program's life, so we can undo.
    # Everytime we perform an operation that modifies data in our program (so commands like 'add', 'remove',
    # 'replace', or 'filter') we need to store the state of the data before the operation, so in case we want
    # to restore the previous state, we can do it.

    states = []
    commands_through_time = []
    current_state = deepcopy(apartments)

    while True:
        try:
            cmd_line = input("Please enter your command\n"
                             "(Enter 'info' if you want to see all available commands)\n")
            # First, parse the cmd_line into something like ('add', [15, 'water', 200])
            cmd, args = fns.parse_command_and_arguments(cmd_line)

            # print(cmd, args)

            # Then, get all the needed arguments for all possible cases into just one variable than we unpack
            # when calling functions. This is done in order to avoid a long if/elif/else block
            args = helper_run_menu_cmd(apartments, commands, cmd, args)

            if cmd == 'exit':
                return

            elif cmd == 'undo':
                apartments, current_state = ui_undo(apartments, states, current_state, commands_through_time)

            elif cmd in commands.keys():
                commands[cmd](*args)

            else:
                print("Invalid command! Try again.")

        except (ValueError, TypeError, IndexError) as err:
            print(str(err))
        # KeyError automatically adds quotation marks, so we treat it separately, ignoring the first and last elements
        except KeyError as ke:
            print(str(ke)[1:-1])

        else:
            if cmd in ['add', 'remove', 'replace', 'occupy', 'clear', 'filter']:
                commands_through_time.append(cmd_line)
                current_state = fns.check_state_change(apartments, states, current_state)

        print()
