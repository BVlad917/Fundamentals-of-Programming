from enum import Enum, unique

from utils.algorithms.bubble_sort import BubbleSort
from utils.algorithms.gnome_sort import GnomeSort
from utils.algorithms.insertion_sort import InsertionSort
from utils.algorithms.merge_sort import MergeSort
from utils.algorithms.selection_sort import SelectionSort


@unique
class Algorithm(Enum):
    # Implemented by me
    SELECTION_SORT = SelectionSort
    GNOME_SORT = GnomeSort

    # From the lecture/seminar
    BUBBLE_SORT = BubbleSort
    INSERTION_SORT = InsertionSort
    MERGE_SORT = MergeSort
