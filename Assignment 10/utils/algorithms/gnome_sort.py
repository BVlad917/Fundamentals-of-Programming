from utils.generic_sort import GenericSort


class GnomeSort(GenericSort):
    def __init__(self, data, key, reverse):
        super().__init__(data, key, reverse)

    def sort(self):
        """
        Gnome sort iterates over the list of elements from a list and compares consecutive elements from this list.
        If the current pairs of elements that are compared are not ordered we swap them and decrease the index that
        helps us iterate over the list, so that any changes that have to be made because of the change that we just
        performed are indeed made. Time complexity O(n^2).
        """
        idx = 0
        while idx < len(self.data):
            if idx == 0 or self._in_order(self.data[idx - 1], self.data[idx]):
                idx += 1
            else:
                self.data[idx], self.data[idx - 1] = self.data[idx - 1], self.data[idx]
                idx -= 1
