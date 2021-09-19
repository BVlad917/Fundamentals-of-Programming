#
# Write the implementation for A2 in this file
#


# ------------------------------------------------------------- #
# -------------------- Non-UI section -------------------------- #
# -------------------------------------------------------------- #
# (write all non-UI functions in this section)
# There should be no print or input statements below this comment
# Each function should do one thing only
# Functions communicate using input parameters and their return values
# print('Hello A2'!) -> prints aren't allowed here!

from random import randint
from math import sqrt


def create_complex(a, b):
    """
    Creates the complex number z = a + bi

    :param a: The real part of the complex number; int
    :param b: The imaginary part of the complex number; int
    :return z: The complex number; dictionary
    """

    # return [a, b]    # Not explicit enough!
    return {"real": a, "imag": b}


def get_real(z):
    """
    Returns the real part of the complex number z

    :param z: The complex number; int
    :return: The real part of z
    """
    # return z[0]
    return z["real"]


def set_real(z, a):
    """
    Sets the real part of the complex number z

    :param z: The complex number; dictionary
    :param a: The new real part of z; int
    """
    # z[0] = a
    z["real"] = a


def get_imaginary(z):
    """
    Returns the imaginary part of the complex number z

    :param z: The complex number; dictionary
    :return: The imaginary part of z
    """
    # return z[1]
    return z["imag"]


def set_imaginary(z, b):
    """
    Sets the imaginary part of the complex number z

    :param z: The complex number; dictionary
    :param b: The new imaginary part; int
    """
    # z[1] = b
    z["imag"] = b


def complex_to_str(z):
    """
    Return the string representation of the complex number z

    :param z: The complex number; dictionary
    :return: z's string representation
    """

    real_part = get_real(z)
    imag_part = get_imaginary(z)

    if imag_part < 0:
        return str(real_part) + " - " + str(abs(imag_part)) + "i"

    return str(real_part) + " + " + str(imag_part) + "i"


# -------------------------- Operations ----------------------#


def compute_modulus(z):
    """
    Finds the modulus of the complex number z

    :param z: The complex number; dictionary
    :return: z's modulus
    """

    return sqrt(get_real(z) * get_real(z) + get_imaginary(z) * get_imaginary(z))


def add_complex(complex_numbers, new_complex):
    """
    Adds new_number to the list of numbers.

    :param complex_numbers: The list of numbers; list
    :param new_complex: The new number, to be added to the list; dictionary
    """

    complex_numbers.append(new_complex)


def generate_random_complex(real_lb=-1000, real_ub=1000, imag_lb=-1000, imag_ub=1000):
    """
    Generates a random complex numbers with the given lower bounds of real/imaginary part, if these are given.
    Else uses the default values.

    :param real_lb: Real part lower bound; int
    :param real_ub: Real part upper bound; int
    :param imag_lb: Imaginary part lower bound; int
    :param imag_ub: Imaginary part upper bound; int
    """

    rand_real = randint(real_lb, real_ub)
    rand_imag = randint(imag_lb, imag_ub)
    return create_complex(rand_real, rand_imag)


def find_all_moduli(complex_numbers):
    """
    Finds the moduli for all the numbers from the list of complex numbers

    :param complex_numbers: The list of complex numbers; list
    :return: A list in which each element is the modulus of the corresponding complex number from the list
    """

    return list(map(compute_modulus, complex_numbers))


def find_longest_seq_of_same_modulus(complex_numbers):
    """
    Returns the longest sequence from the list of complex numbers, in which all elements have the same modulus.

    :param complex_numbers: The list of complex numbers; list
    :return longest_seq: The longest sequence of the list in which all elements have the same modulus; list
    """

    moduli = find_all_moduli(complex_numbers)  # Each element's modulus

    groups = [[complex_numbers[0]]]

    for index in range(1, len(moduli)):
        if moduli[index] == moduli[index - 1]:
            groups[-1].append(complex_numbers[index])
        else:
            groups.append([complex_numbers[index]])

    return max(groups, key=len)


# Z = [z1, z2, z3, z4, z5, z6, z7, z8, z9, z10]
# moduli = [2, 5, 5, 5, 6, 7, 4, 4, 4, 4]
#
# => groups = [[z1], [z2, z3, z4], [z5], [z6], [z7, z8, z9, z10]]
# => max(groups, key=len) = [z7, z8, z9, z10]


# a = create_complex(5, 10)
# b = create_complex(10, -5)
# c = create_complex(12, -13)
# d = create_complex(-13, -12)
# e = create_complex(12, 13)
# f = create_complex(2, -20)
# complexes = [a, b, c, d, e, f]
# print(find_longest_seq_of_same_modulus(complexes))


def find_longest_sequence_incr_modulus(complex_numbers):
    """
    Finds the longest sequence from the list of complex numbers in which the moduli of the elements are increasing.

    :param complex_numbers: The list of complex numbers; dictionary
    :return longest_seq: The longest sequence of the list whose elements have increasing moduli; list
    """

    moduli = find_all_moduli(complex_numbers)  # Each element's modulus

    groups = [[complex_numbers[0]]]

    for index in range(1, len(moduli)):
        if moduli[index] > moduli[index - 1]:
            groups[-1].append(complex_numbers[index])
        else:
            groups.append([complex_numbers[index]])

    return max(groups, key=len)


# Z = [z1, z2, z3, z4, z5, z6, z7, z8, z9, z10]
# moduli = [3, 4, 2, 4, 6, 7, 8, 2, 2, 4]
#
# => groups = [[z1, z2], [z3, z4, z5, z6, z7], [z8, z9, z10]]
# => max(groups, key=len) = [z3, z4, z5, z6, z7]


# a = create_complex(2, 3)
# b = create_complex(3, 4)
# c = create_complex(1, 2)
# d = create_complex(1, 3)
# e = create_complex(7, 8)
# f = create_complex(2, 3)
# complexes = [a, b, c, d, e, f]
# print(find_longest_sequence_incr_modulus(complexes))


def parse_input_list(new_numbers):
    """
    Parses the list of new numbers input from the user into a list of new complex numbers

    :param new_numbers: string; the new list of numbers, from the user
    :return: A list of complex numbers
    """

    numbers_to_add = []
    tokens = new_numbers.split(',')
    tokens = [token.strip() for token in tokens]

    for token in tokens:
        token = token.replace('+', ' +')
        token = token.replace('-', ' -')
        parts = token.split(' ')
        parts = [part for part in parts if part != '' and part != '+' and part != '-']

        if len(parts) == 3:
            i_index = parts.index('i')  # raises ValueError if not found

            if i_index == 0:
                raise ValueError("Please input the complex number in the format 'a+bi'.")

            parts[i_index - 1] = parts[i_index - 1] + parts[i_index]
            parts.remove('i')

        if len(parts) == 2:
            if 'i' in parts[1] and 'i' not in parts[0]:
                real_part, imag_part = parts[0], parts[1]

            elif 'i' in parts[0] and 'i' not in parts[1]:
                real_part, imag_part = parts[1], parts[0]

            else:
                raise ValueError("Please input the complex number in the format 'a+bi'.")

            if imag_part == '+i' or imag_part == '-i':
                imag_part = imag_part[0] + '1' + imag_part[1]

        else:
            nr = parts[0]
            real_part, imag_part = '0', '0'
            if 'i' in nr:
                imag_part = nr
                if imag_part == 'i':
                    imag_part = '1i'
                elif imag_part == '-i':
                    imag_part = '-1i'

            else:
                real_part = nr

        imag_part = imag_part.replace("i", "")
        numbers_to_add.append(create_complex(int(real_part), int(imag_part)))

    return numbers_to_add


# -------------------------------------------------------------- #
# ------------------------ UI section -------------------------- #
# -------------------------------------------------------------- #
# (write all functions that have input or print statements here). 
# Ideally, this section should not contain any calculations relevant to program functionalities


def ui_print_menu():
    print("Possible commands:")
    print("\t1 - Read a list of complex numbers and add them to the list.")
    print("\t2 - Display the entire list of complex numbers.")
    print("\t3 - Display the longest sequence of numbers from the list that have the same modulus.")
    print("\t4 - Display the longest sequence of numbers from the list that have increasing modulus.")
    print("\tx - Exit.")


def ui_read_complex():
    """
    Reads complex number from the user

    :return: New complex number; dictionary
    """

    real = input("Real part: ")
    imag = input("Imaginary part: ")
    return create_complex(int(real), int(imag))


def ui_print_complex(z):
    """
    Prints the complex number z to the console

    :param z: The complex number; dictionary
    """

    print(complex_to_str(z))


def ui_add_to_list(complex_numbers, new_complex=None):
    """
    Adds a new complex number to the list of complex numbers

    :param complex_numbers: The list of complex numbers; list
    :param new_complex: If given, can add this complex number without reading it; dictionary
    """

    if new_complex is None:
        new_complex = ui_read_complex()

    add_complex(complex_numbers, new_complex)
    print("Added the complex number " + complex_to_str(new_complex) + " to the list.")


def ui_add_multiple_elements(complex_numbers):
    """
    Adds a list of input complex numbers from the console

    :param complex_numbers: The list of complex numbers; list
    """

    new_numbers = input("Please give a few complex numbers separated by a comma: ")
    numbers_to_add = parse_input_list(new_numbers)

    for number in numbers_to_add:
        ui_add_to_list(complex_numbers, number)


def ui_populate_list(complex_numbers, populate_with=10, real_lb=-100, real_ub=100, imag_lb=-100, imag_ub=100):
    """
    Populates the list of complex numbers with random complex numbers.

    :param complex_numbers: The list of complex numbers
    :param populate_with: How many random complex numbers to add to the list; int
    :param imag_lb: The lower bound of the imaginary part of the random complex number to generate; int
    :param imag_ub: The upper bound - // --; int
    :param real_lb: The lower bound of the real part  -- // --; int
    :param real_ub: The upper bound  -- // --; int
    """

    for _ in range(populate_with):
        new_complex = generate_random_complex(real_lb, real_ub, imag_lb, imag_ub)
        add_complex(complex_numbers, new_complex)

    print("Added {} random complex numbers to the list.\n".format(populate_with))


def ui_print_full_list(complex_numbers):
    """
    Prints the full list of complex numbers

    :param complex_numbers: The list of complex numbers; list
    """

    print("These are all the complex numbers from the list:")

    for index, complex_number in enumerate(complex_numbers):
        print("\t" + str(index + 1) + ") ", end="")
        ui_print_complex(complex_number)


def ui_print_longest_seq_same_modulus(complex_numbers):
    """
    Prints the longest sequence with the same modulus from the list of complex numbers.
    If more sequences with the same length present, returns the first one.

    :param complex_numbers: The list of complex numbers; list
    """

    longest_sequence = find_longest_seq_of_same_modulus(complex_numbers)

    print("This is the longest sequence whose elements have the same modulus:")
    print("(Modulus = {})".format(compute_modulus(longest_sequence[0])))

    for index, complex_number in enumerate(longest_sequence):
        print("\t" + str(index + 1) + ") ", end="")
        ui_print_complex(complex_number)


def ui_print_longest_incr_modulus(complex_numbers):
    """
    Prints the longest sequence (from the list of complex numbers) whose elements have increasing moduli.
    If more sequences of same length present, returns the first one.

    :param complex_numbers: The list of complex numbers
    """

    longest_sequence = find_longest_sequence_incr_modulus(complex_numbers)

    print("This is the longest sequence whose elements have increasing moduli:")

    for index, complex_number in enumerate(longest_sequence):
        print("\t" + str(index + 1) + ") ", end="")
        ui_print_complex(complex_number)


def start():
    """
    Handles the user interface

    :return: Returns once the program is finished
    """

    complex_numbers = []
    commands = {'1': ui_add_multiple_elements, '2': ui_print_full_list,
                '3': ui_print_longest_seq_same_modulus, '4': ui_print_longest_incr_modulus}

    ui_populate_list(complex_numbers)

    while True:

        try:
            ui_print_menu()
            option = input("Enter operation: ")

            if option in commands.keys():
                commands[option](complex_numbers)

            elif option == 'x':
                return

            else:
                print("Invalid command.")

        except ValueError as ve:
            print("Error: " + str(ve))

        print("")


if __name__ == "__main__":
    """
    Display on the console the longest sequence that observes a given property
        Property 3. Numbers having the same modulus.
        Property 4. Numbers having increasing modulus.
    """

    print("Hello!\n")

    start()

    print("Bye!")
