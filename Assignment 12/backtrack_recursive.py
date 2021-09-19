"""
12. Consider the natural number n (n<=10) and the natural numbers a1, ..., an. Determine all the possibilities to
insert between all numbers a1, ..., an the operators + and – such that by evaluating the expression the
result is positive.
"""


def consistent(signs, nums):
    return len(signs) <= len(nums) - 1


def first_sign():
    return '+'


def next_sign(signs):
    return '-' if signs[-1] == '+' else None


def generate_expression_str(signs, nums):
    fn_str = ""
    for index in range(len(signs)):
        fn_str = fn_str + str(nums[index]) + signs[index]
    fn_str = fn_str + str(nums[-1])
    return fn_str


def is_solution(signs, nums):
    if len(signs) != len(nums) - 1:
        return False
    return True if eval(generate_expression_str(signs, nums)) > 0 else False


def print_solution(signs, nums):
    expression_str = generate_expression_str(signs, nums)
    print(expression_str + "=" + str(eval(expression_str)))


# def backtrack(signs, nums):
#     new_sign = first_sign()
#     signs.append(new_sign)
#     while new_sign is not None:
#         if consistent(signs, nums):
#             if is_solution(signs, nums):
#                 print_solution(signs, nums)
#             else:
#                 backtrack(signs[:], nums)
#         new_sign = next_sign(signs)
#         signs[-1] = new_sign


def backtrack(signs, nums):
    signs.append(None)  # Create a new space in the list (for a new sign)
    for sign in ('+', '-'):
        signs[-1] = sign
        if consistent(signs, nums):
            if is_solution(signs, nums):
                print_solution(signs, nums)
            else:
                backtrack(signs[:], nums)
        else:
            break


if __name__ == '__main__':
    n = int(input("Give the number n: "))
    numbers = []
    for i in range(n):
        a = int(input(f"Give the number from index {i}: "))
        numbers.append(a)
    backtrack([], numbers)
