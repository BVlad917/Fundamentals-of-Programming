#
# Implement the program to solve the problem statement from the second set here
#

# Set 2, Problem 6
# The numbers n1 and n2 have the property P if their writing in base 10 uses the same digits (e.g. 2113 and 323121).
# Determine whether two given natural numbers have property P.


def digits_in_number(num):
    """
    Find which digits does the number num have

    :param num: the number whose digits we will find, natural number
    :return digits_0_to_9: a list of 10 bool values where each index denotes whether or not the input number 'n'
                            has the digit corresponding to that index
    """

    digits_0_to_9 = [False] * 10  # Defines a list of length 10, each value being the bool value False

    while num:
        digits_0_to_9[num % 10] = True
        num = num // 10

    return digits_0_to_9


def check_property_p(num1, num2):
    """
    Checks whether or not the two input numbers num1 and num2 have property P.

    :param num1: The first input number, natural number
    :param num2: The second input number, natural number
    :return True/False: depending on whether or not the two numbers have property P
    """

    num1_digits = digits_in_number(num1)
    num2_digits = digits_in_number(num2)

    # The list that will consider simultaneous existence/non-existence of digits in num1 and num2
    sim_digit_presence = []

    for num1_digit, num2_digit in zip(num1_digits, num2_digits):
        sim_digit_presence.append(num1_digit - num2_digit)

    # The bellow command returns False if sim_digit_presence contains (on any index) -1 or 1. This is the right
    # thing, since we want sim_digit_presence to contain zeros only, else the 2 numbers DON'T have property P
    return not any([bad_value in sim_digit_presence for bad_value in [-1, 1]])


if __name__ == "__main__":
    n1 = int(input("Please input the first number: "))
    n2 = int(input("Please input the second number: "))

    # Throws an AssertionError if any of the two numbers are negative
    assert n1 >= 0 and n2 >= 0, "Please run the program again and input two natural numbers"

    if check_property_p(n1, n2):
        print("The numbers " + str(n1) + " and " + str(n2) + " have property P.")
    else:
        print("The numbers " + str(n1) + " and " + str(n2) + " do not have property P.")
