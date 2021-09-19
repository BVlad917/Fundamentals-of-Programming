from utils.generic_sort import GenericSort


class MergeSort(GenericSort):
    def __init__(self, data, key, reverse):
        super().__init__(data, key, reverse)

    def sort(self):
        self.data[:] = self.__merge_sort(self.data)

    def __merge_sort(self, my_data):
        if len(my_data) <= 1:
            return my_data
        m = len(my_data) // 2
        left = self.__merge_sort(my_data[:m])
        right = self.__merge_sort(my_data[m:])
        return self.__merge(left, right)

    def __merge(self, left, right):
        rez = []
        while len(left) > 0 and len(right) > 0:
            if self._in_order(left[0], right[0]):
                rez.append(left.pop(0))
            else:
                rez.append(right.pop(0))
        rez.extend(left + right)
        return rez
