from domain.validators import UndoException, UndoRedoException, RedoException


class UndoRedoRepository:
    """
    Generic repository used for both the undo and redo stacks
    """
    def __init__(self):
        self.__undo_or_redo_stack = []

    def __len__(self):
        return len(self.__undo_or_redo_stack)

    # def __str__(self):
    #     return str(self.__undo_or_redo_stack)

    def check_empty(self):
        """
        Checks if the stack is empty. If it is, it raises an UndoRedoException (generic exception)
        """
        if len(self) == 0:
            raise UndoRedoException("The operation stack is empty!")

    def record_inverse_operations(self, fn, *args):
        """
        Appends a new inverse function (and its arguments) on the stack
        """
        self.__undo_or_redo_stack.append((fn, args))

    def get_reverse_operation(self):
        """
        Pops the last inserted function on the stack and returns it
        """
        return self.__undo_or_redo_stack.pop()

    def clear_stack(self):
        """
        Empties the stack
        """
        self.__undo_or_redo_stack.clear()

    def see_top_of_stack(self):
        """
        Returns the (inverse_function, *args) tuple from the top of the stack. Notice: Different from
        the function get_reverse_operation(), as this function doesn't pop the top element from the stack.
        """
        return self.__undo_or_redo_stack[-1]


class UndoRepository(UndoRedoRepository):
    """
    Class used for the Undo stack. It subclasses the generic UndoRedoRepository class.
    """
    def check_empty(self):
        if len(self) == 0:
            raise UndoException("The undo stack is empty! Cannot undo anymore.")


class RedoRepository(UndoRedoRepository):
    """
    Class used for the Redo stack. It subclasses the generic UndoRedoRepository class.
    """
    def check_empty(self):
        if len(self) == 0:
            raise RedoException("The redo stack is empty! Cannot redo anymore.")
