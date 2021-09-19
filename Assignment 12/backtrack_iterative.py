"""
12. Consider the natural number n (n<=10) and the natural numbers a1, ..., an. Determine all the possibilities to
insert between all numbers a1, ..., an the operators + and – such that by evaluating the expression the
result is positive.
"""


def initial_value():
    return 0


def next_element(signs):
    if signs[-1] == 0:
        return '+'
    if signs[-1] == '+':
        return '-'
    if signs[-1] == '-':
        return None


def generate_expression_str(signs, nums):
    fn_str = ""
    for index in range(len(signs)):
        fn_str = fn_str + str(nums[index]) + signs[index]
    fn_str = fn_str + str(nums[-1])
    return fn_str


def consistent(signs, nums):
    return len(signs) <= len(nums) - 1


def is_solution(signs, nums):
    if len(signs) != len(nums) - 1:
        return False
    return True if eval(generate_expression_str(signs, nums)) > 0 else False


def print_solution(signs, nums):
    expression_str = generate_expression_str(signs, nums)
    print(expression_str + "=" + str(eval(expression_str)))


def backtrack(nums):
    signs = [initial_value()]
    while len(signs) > 0:
        el = next_element(signs)
        while el is not None:
            signs[-1] = el
            if consistent(signs, nums):
                if is_solution(signs, nums):
                    print_solution(signs, nums)
                else:
                    if len(signs) == len(nums) - 1:
                        signs = signs[:-1]
                    else:
                        signs.append(initial_value())
                        break
            el = next_element(signs)
        if el is None:
            signs = signs[:-1]


if __name__ == '__main__':
    n = int(input("Give the number n: "))
    numbers = []
    for ind in range(n):
        a = int(input(f"Give the number with index {ind}: "))
        numbers.append(a)
    backtrack(numbers)
