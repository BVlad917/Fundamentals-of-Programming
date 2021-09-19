#
# Implement the program to solve the problem statement from the third set here
#

# Set 3, Problem 4
# Generate the largest perfect number smaller than a given natural number n. If such a number does not exist,
# a message should be displayed. A number is perfect if it is equal to the sum of its divisors, except itself.
# (e.g. 6 is a perfect number, as 6=1+2+3).

from math import sqrt


def sum_of_divisors_except_input(x):
    """
    Finds the sum of x's divisors (without adding the divisor x itself)

    :param x: the number whose divisors' sum we want to find, natural number
    :return sum: the sum of x's divisors (without adding the divisor x itself to the sum)
    """

    sum_of_divs = 0

    for div in range(1, int(sqrt(x)) + 1):
        if x % div == 0:

            # If x is a perfect square we don't want to add its square root twice (e.g., Don't add 3 twice for x=9)
            # The following if-else statement handles this case

            if div == x / div:
                sum_of_divs = sum_of_divs + div
            else:
                sum_of_divs = sum_of_divs + div
                sum_of_divs = sum_of_divs + int(x / div)  # Convert x/div into int so sum_of_divs is int, not float

    # During the for loop we also added the divisor x, so now we need to subtract it
    sum_of_divs = sum_of_divs - x

    return sum_of_divs


def check_if_perfect(x):
    """
    Checks whether x is a perfect number or not
    :param x: the number we have to check if it is a perfect number of not; natural number
    :return True/False: if the number x is a perfect number, returns True. Else returns False
    """

    return sum_of_divisors_except_input(x) == x


def largest_perfect_smaller_than_input(x):
    """
    Finds the largest perfect number that is smaller than the input number x

    :param x: We have to find the largest perfect number smaller than this x; natural number
    :return: (True, <largest_perfect>) or (False, None) if there is no perfect number smaller than x
    """

    for candidate in range(x - 1, 5, -1):    # No reason to go lower, 6 is the smallest perfect number
        if check_if_perfect(candidate):
            return True, candidate

    return False, None


if __name__ == "__main__":
    n = int(input("Please input the number n: "))

    assert n >= 0, "Please run the program again and input a natural number"

    found_perfect_number, perfect_number = largest_perfect_smaller_than_input(n)

    if found_perfect_number:
        print("The largest perfect number smaller than " + str(n) + " is " + str(perfect_number))
    else:
        print("There is no perfect number smaller than " + str(n))
