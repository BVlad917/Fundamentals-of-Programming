from utils.generic_sort import GenericSort


class BubbleSort(GenericSort):
    def __init__(self, data, key, reverse):
        super().__init__(data, key, reverse)

    def sort(self):
        while True:
            sw = True
            for i in range(len(self.data) - 1):
                if not self._in_order(self.data[i], self.data[i+1]):
                    self.data[i], self.data[i+1] = self.data[i+1], self.data[i]
                    sw = False
            if sw: break