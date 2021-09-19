class UndoService:
    """

    """
    def __init__(self, undo_repo, double_pop_fns, double_pop_fns_counter_part):
        self.__undo_repo = undo_repo
        self.__double_pop_fns = double_pop_fns
        self.__double_pop_counter_part = double_pop_fns_counter_part

    def apply_undo(self):
        self.__undo_repo.check_empty()

        fn, args = self.__undo_repo.get_reverse_operation()
        fn(*args, record_undo=False, record_redo=True)

        if fn in self.__double_pop_fns and len(self.__undo_repo) and \
                self.__undo_repo.see_top_of_stack()[0] in self.__double_pop_counter_part:
            fn2, args2 = self.__undo_repo.get_reverse_operation()
            fn2(*args2, record_undo=False, record_redo=True)

    def record_inverse_operations(self, fn, *args):
        self.__undo_repo.record_inverse_operations(fn, *args)
