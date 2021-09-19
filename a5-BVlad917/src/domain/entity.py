"""
    Module used for representing the main entities of the program. Currently contains the representation of
    the complex number entity (the representation is done through a class).
"""


class ComplexNumber:
    """
    Class for the complex number entities.
    The list of complex numbers will contain instances of this class.

    :param real: Real part of the complex number to be generated; integer
    :param imag: Imaginary part of the complex number to be generated; integer
    """

    def __init__(self, real=0, imag=0):
        self.real = real
        self.imag = imag

    def __repr__(self):
        """
        We overwrite the __repr__ built-in method such that when we want to print a complex number, or when we
        want to print the list of complex numbers, we will get a string representation of the number, and not
        an object's address.
        :return: string representing the complex number
        """
        # We have 2 edge cases we need to take care of separately
        if self.real == 0 and self.imag == 1:
            return 'i'
        elif self.real == 0 and self.imag == -1:
            return '-i'

        real_part = str(self.real) if self.real != 0 else ''
        imag_part = str(self.imag) + 'i' if self.imag != 0 else ''
        imag_part_sign = '+' if self.imag > 0 and self.real != 0 else ''
        return real_part + imag_part_sign + imag_part

    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    @property
    def real(self):
        return self.__real

    @real.setter
    def real(self, real):
        self.__real = real

    @property
    def imag(self):
        return self.__imag

    @imag.setter
    def imag(self, imag):
        self.__imag = imag
