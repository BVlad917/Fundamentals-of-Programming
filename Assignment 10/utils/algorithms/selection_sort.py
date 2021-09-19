from utils.generic_sort import GenericSort


class SelectionSort(GenericSort):
    def __init__(self, data, key, reverse):
        super().__init__(data, key, reverse)

    def sort(self):
        """
        Selection sort iterates over every element from the list with one for loop, and with another for loop goes
        over every element to the right of the current element of the initial for loop and swaps the minimum element
        from this part of the list with the current element in that initial for loop. Essentially, for every element
        of the list we select the minimum element from the rest of the list right to it and swap these elements.
        Time complexity: O(n^2).
        """
        for i in range(len(self.data) - 1):
            for j in range(i+1, len(self.data)):
                if not self._in_order(self.data[i], self.data[j]):
                    self.data[i], self.data[j] = self.data[j], self.data[i]
