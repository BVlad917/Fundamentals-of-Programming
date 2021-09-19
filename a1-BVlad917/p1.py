#
# Implement the program to solve the problem statement from the first set here
#

# Set 1, Problem 5
# Generate the largest prime number smaller than a given natural number n. If such a number does not exist,
# a message should be displayed.

from math import sqrt


def check_prime(a):
    """
    Checks if the input natural number a is prime or not

    :param a: the number that we want to determine whether or not is true, natural number
    :return True/False: depending on the primality of the number a
    """

    if a == 2:
        return True
    if a <= 1 or a % 2 == 0:
        return False

    for div in range(3, int(sqrt(a)) + 1, 2):
        if a % div == 0:
            return False

    return True


def prime_smaller_than_input(a):
    """
    Determines the largest prime smaller than a given number a

    :param a: the input (natural) number; we want to find the largest prime smaller than this a
    :return: (True, <largest_prime_number>) or (False, None) if there is no prime smaller than a
    """

    for x in range(a - 1, 1, -1):
        if check_prime(x):
            return True, x

    return False, None


if __name__ == "__main__":
    n = int(input("Please input the number n: "))

    # This will throw an AssertionError, asking for a natural number
    assert n >= 0, "Please run the program again and input a natural number, not an integer"

    found_largest_prime_smaller_than_n, largest_prime_smaller_than_n = prime_smaller_than_input(n)

    if found_largest_prime_smaller_than_n:
        print("The largest prime smaller than " + str(n) + " is " + str(largest_prime_smaller_than_n))
    else:
        print("There is no prime number smaller than " + str(n))
