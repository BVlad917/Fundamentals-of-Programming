class RedoService:
    def __init__(self, redo_repo, double_pop_fns, double_pop_fns_counter_part):
        self.__redo_repo = redo_repo
        self.__double_pop_fns = double_pop_fns
        self.__double_pop_fns_counter_part = double_pop_fns_counter_part

    def apply_redo(self):
        self.__redo_repo.check_empty()
        fn, args = self.__redo_repo.get_reverse_operation()
        fn(*args, record_undo=True, record_redo=False, as_redo=True)

        if fn in self.__double_pop_fns and len(self.__redo_repo) and \
                self.__redo_repo.see_top_of_stack()[0] in self.__double_pop_fns_counter_part:
            fn2, args2 = self.__redo_repo.get_reverse_operation()
            fn2(*args2, record_undo=True, record_redo=False, as_redo=True)

    def record_inverse_operations(self, fn, *args):
        self.__redo_repo.record_inverse_operations(fn, *args)
