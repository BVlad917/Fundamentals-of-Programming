from domain.entity_with_id import EntityWithID


class Person(EntityWithID):
    """
    Class representing the Person entity
    :param person_id: The ID to be assigned to the person
    :param name: The name of the person
    :param phone_number: The phone number of the person
    """

    def __init__(self, person_id, name, phone_number):
        super().__init__(person_id)
        self.name = name.title()
        self.phone_number = phone_number

    def __eq__(self, other):
        """
        Used to check if two persons entities are referring to the same person
        :param other: a person entity to compare this person to
        """
        return self.id == other.id and self.name == other.name and self.__phone_number == self.phone_number

    def __repr__(self):
        """
        Internal representation of the person entity; Used for unambiguity
        """
        return f"PersonID({self.id});PersonName({self.name});PersonPhoneNumber({self.phone_number})"

    def __str__(self):
        """
        Surface representation of the person entity; Used for user friendly printing
        """
        return f"Person ID: {self.id}\n" \
               f"\tName: {self.name}\n" \
               f"\tPhone Number: {self.phone_number}\n"

    def json_dump(self):
        return {'Person': {
            'id': self.id,
            'name': self.name,
            'phone': self.phone_number
        }}

    @staticmethod
    def json_load(dumped_obj):
        # print(dumped_obj['Person'])
        return Person(dumped_obj['Person']['id'],
                      dumped_obj['Person']['name'],
                      dumped_obj['Person']['phone'])

    @property
    def name(self):
        """
        Returns the name of the person as a string
        """
        return self.__name

    @name.setter
    def name(self, pers_name):
        """
        Setter for the person's name
        :param pers_name: String to be set as the person's name
        """
        self.__name = pers_name

    @property
    def phone_number(self):
        """
        Returns the phone number of the person as a string
        """
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, pers_phone_num):
        """
        Setter for the phone number of the person
        :param pers_phone_num: Phone number as a string to be set as the person's phone number
        """
        self.__phone_number = pers_phone_num
