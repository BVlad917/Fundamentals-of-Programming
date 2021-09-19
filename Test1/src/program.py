import re


def create_fn(func_name, func_params, signs):
    return {"func_name": func_name, "func_params": func_params, "func_signs": signs}


def get_fn_name(fn):
    return fn["func_name"]


def get_fn_params(fn):
    return fn["func_params"]


def get_fn_signs(fn):
    return fn["func_signs"]


def set_fn_name(fn, name):
    fn["func_name"] = name


def set_fn_eval(fn, definition):
    fn["func_eval"] = definition


def set_fn_params(fn, params):
    fn["func_params"] = params


def parse_func_def(func_def):
    first_paran = func_def.find('(')
    second_paran = func_def.find(')')
    equal_sign = func_def.find('=')
    func_name = func_def[:equal_sign]
    params = func_def[first_paran + 1:second_paran].split(',')
    signs_between_params = re.findall(r"[+-]", func_def)

    # print(func_name)
    # print(params)
    # print(signs_between_params)
    return func_name, params, signs_between_params


def create_fn_operation(fn):
    signs = get_fn_signs(fn)
    params = get_fn_params(fn)

    if len(params) == 1:
        evaluation = signs[0] + params[0]

    else:
        evaluation = params[0]
        for param, sign in zip(params[1:], signs):
            evaluation = evaluation + sign + param

    return evaluation


def add_fn(fns, function):
    """
    Adds a new function to the list of functions
    :param fns: The list of functions
    :param function: The string representing the new function to be added
    :return: -
    """
    func_name, params, signs_between_params = parse_func_def(function)
    new_fn = create_fn(func_name, params, signs_between_params)
    # print(new_fn)
    # print(get_fn_name(new_fn))
    fns.append(new_fn)


def find_fn_in_list_of_fns(fns, function_name):
    function_names_with_params = [get_fn_name(fn) for fn in fns]
    function_names_no_params = []
    for function_name in function_names_with_params:
        parantheses_index = function_name.find('(')
        function_names_no_params.append(function_name[:parantheses_index])

    index = next((index for index, fn_name in enumerate(function_names_no_params) if function_name == fn_name), None)
    return index


def list_fn(fns, function):
    # print(function)
    fn_index = find_fn_in_list_of_fns(fns, function)
    if fn_index is None:
        raise ValueError("The function is not in the list!")

    function_to_show = fns[fn_index]
    operation = create_fn_operation(function_to_show)

    return f"def {get_fn_name(function_to_show)}: return {operation}"


def eval(fns, params):
    space_ind = params.index(' ')
    open_paran_ind = params.index('(')
    close_paran_ind = params.index(')')

    func_params = params[open_paran_ind+1:close_paran_ind]
    func_name = params[space_ind+1:open_paran_ind]

    in_list_index = find_fn_in_list_of_fns(fns, func_name)
    if in_list_index is None:
        raise ValueError("The function is not in the list!")

    eval_func = fns[in_list_index]
    fn_operation = create_fn_operation(eval_func)
    #todo: have to complete this


def ui_list_fn(fns, function):
    function_def = list_fn(fns, function)
    print(function_def)


def run_menu():
    fns = []
    commands = {'add': None, 'list': None, 'eval': None}

    while True:
        try:
            cmd = input("Please enter a command\nEnter x to exit: ")

            cmd = cmd.strip()

            if cmd == 'x':
                break

            space_index = cmd.find(' ')
            if space_index == -1:
                raise ValueError("Incorrect input")

            command = cmd[:space_index].lower().strip()
            function = cmd[space_index + 1:].lower().strip()

            # print(func_name)
            # print(func_def)

            if command not in commands.keys():
                raise ValueError("The command is not currently supported.")

            if command == 'add':
                add_fn(fns, function)
            elif command == 'list':
                ui_list_fn(fns, function)
            elif command == 'eval':
                pass


        except ValueError as ve:
            print(str(ve))


run_menu()
