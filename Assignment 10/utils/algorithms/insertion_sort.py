from utils.generic_sort import GenericSort


class InsertionSort(GenericSort):
    def __init__(self, data, key, reverse):
        super().__init__(data, key, reverse)

    def sort(self):
        for i in range(1, len(self.data)):
            p = self.data[i]
            j = i - 1
            while j >= 0 and self._in_order(p, self.data[j]):
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = p
