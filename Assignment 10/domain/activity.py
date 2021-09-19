from domain.entity_with_id import EntityWithID
from domain.validators import DateTimeValidator


class Activity(EntityWithID):
    """
    Class representing the Activity entity
    :param activity_id: The id given to the activity; positive integer
    :param start_date_time: The date and time when the activity starts; datetime.datetime variable
    :param end_date_time: The date and time when the activity ends; datetime.datetime variable
    :param description: Description of the activity; string
    :param persons_id: The IDs of the persons registered in this activity; list of positive integers
    """

    def __init__(self, activity_id, start_date_time, end_date_time, description="", persons_id=None):
        super().__init__(activity_id)
        self.__persons_id = [] if persons_id is None else persons_id
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.description = description

    def __eq__(self, other):
        return self.id == other.id and self.persons_id == other.persons_id and \
               self.start_date_time == other.start_date_time and self.end_date_time == other.end_date_time and \
               self.description == other.description

    def __str__(self):
        """
        String, user-friendly representation of the activity
        Different string format depending on whether or not the activity starts and ends on the same day
        :return: The string representation of the activity
        """
        if self.start_year == self.end_year and \
                self.start_month == self.end_month and \
                self.start_day == self.end_day:
            return f"Activity ID {self.id}\n" \
                   f"\tDescription of the activity: {self.description}\n" \
                   f"\tIDs of the persons signed up for this activity: " \
                   f"{', '.join(str(id_) for id_ in self.persons_id)}\n" \
                   f"\tDate of the activity: {self.start_year}/{self.start_month}/{self.start_day}\n" \
                   f"\tTime interval of the activity: {str(self.start_hour).zfill(2)}:" \
                   f"{str(self.start_minute).zfill(2)} - {str(self.end_hour).zfill(2)}:{str(self.end_minute).zfill(2)}"

        return f"Activity ID {self.id}\n" \
               f"\tDescription of the activity: {self.description}\n" \
               f"\tIDs of the persons signed up for this activity: " \
               f"{', '.join(str(id_) for id_ in self.persons_id)}\n" \
               f"\tTime interval of the activity: {self.start_date_time.strftime('%Y/%m/%d %H:%M')}" \
               f" - {self.end_date_time.strftime('%Y/%m/%d %H:%M')}"

    def __repr__(self):
        """
        Internal representation of the activity; meant to be unambiguous
        :return: The string meant for internal representation
        """
        return f"Activity ID: {self.id}; Person IDs: {self.persons_id}; Start time: {self.start_date_time};" \
               f"End time: {self.end_date_time}; Description: {self.description}"

    def json_dump(self):
        return {'Activity': {
            'id': self.id,
            'start': self.start_date_time.strftime("%d/%m/%Y %H:%M"),
            'end': self.end_date_time.strftime("%d/%m/%Y %H:%M"),
            'description': self.description,
            'persons': self.persons_id
        }}

    @staticmethod
    def json_load(dumped_obj):
        start_date_str = dumped_obj['Activity']['start']
        end_date_str = dumped_obj['Activity']['end']
        start_datetime = DateTimeValidator.validate(*start_date_str.split())
        end_datetime = DateTimeValidator.validate(*end_date_str.split())
        return Activity(dumped_obj['Activity']['id'],
                        start_datetime,
                        end_datetime,
                        dumped_obj['Activity']['description'],
                        dumped_obj['Activity']['persons'])

    def get_all_person_ids_in_activity(self):
        """
        Returns all the IDs of the persons involved in this activity as a list of integers
        """
        return self.persons_id

    def add_person_id(self, person_id):
        """
        Adds <person_id> to the list of registered person IDs for this activity
        :param person_id: The ID of the person to be added; positive integer
        """
        self.persons_id.append(person_id)

    def remove_person_id(self, person_id):
        """
        Removes <person_id> from the list of registered person IDs for this activity
        :param person_id: The ID of the person to be removed; positive integer
        """
        self.persons_id.remove(person_id)

    def change_start_date(self, new_start_date):
        """
        Changes the starting date information (date and time) to a new datetime variable
        :param new_start_date: The new datetime variable that the activity will have as a starting datetime
        """
        self.start_date_time = new_start_date

    def change_end_date(self, new_end_date):
        """
        Changes the ending date information (date and time) to a new datetime variable
        :param new_end_date: The new datetime variable that the activity will have as an ending datetime
        """
        self.end_date_time = new_end_date

    def change_description(self, new_description):
        """
        Changes the description of the activity to a new description
        :param new_description: The string to be used as the new activity description
        """
        self.description = new_description

    @property
    def persons_id(self):
        """
        Getter for the list of persons registered for the activity
        :return: List of positive integers; IDs of the persons registered for the activity
        """
        return self.__persons_id

    @property
    def start_date_time(self):
        """
        Returns the starting date and time of the activity
        :return: Datetime variable representing the starting date and time of the activity
        """
        return self.__start_date_time

    @start_date_time.setter
    def start_date_time(self, activity_start_date_time):
        """
        Setter for the starting date and time of the activity
        :param activity_start_date_time: Datetime variable to be set as the new activity starting date and time
        """
        self.__start_date_time = activity_start_date_time

    @property
    def start_hour(self):
        """
        Getter for the starting hour of the activity
        :return: The hour at which the activity starts; positive integer in range [0, 23]
        """
        return self.start_date_time.hour

    @start_hour.setter
    def start_hour(self, new_hour):
        """
        Setter for the starting hour of the activity
        :param new_hour: The hour to be set as the new starting hour; positive integer in range [0, 23]
        """
        self.start_date_time = self.start_date_time.replace(hour=new_hour)

    @property
    def start_minute(self):
        """
        Getter for the starting minute of the activity
        :return: The minute at which the activity starts; positive integer in range [0, 59]
        """
        return self.start_date_time.minute

    @start_minute.setter
    def start_minute(self, new_minute):
        """
        Setter for the starting minute of the activity
        :param new_minute: The minute to be set as the new starting minute; positive integer in range [0, 59]
        """
        self.start_date_time = self.start_date_time.replace(minute=new_minute)

    @property
    def start_day(self):
        """
        Getter for the starting day of the activity
        :return: The day when the activity starts; positive integer in range [1, 31]
        """
        return self.start_date_time.day

    @start_day.setter
    def start_day(self, new_day):
        """
        Setter for the starting day of the activity
        :param new_day: The day to be set as the new starting day of the activity; positive integer in range [1, 31]
        """
        self.start_date_time = self.start_date_time.replace(day=new_day)

    @property
    def start_month(self):
        """
        Getter for the starting month of the activity
        :return: The month when the activity starts; positive integer in range [1, 12]
        """
        return self.start_date_time.month

    @start_month.setter
    def start_month(self, new_month):
        """
        Setter for the starting month of the activity
        :param new_month: The month to be set as the new starting month of the activity;
        positive integer in range [1, 12]
        """
        self.start_date_time = self.start_date_time.replace(month=new_month)

    @property
    def start_year(self):
        """
        Getter for the starting year of the activity
        :return: The year when the activity starts; positive integer >= current, real-life year
        """
        return self.start_date_time.year

    @start_year.setter
    def start_year(self, new_year):
        """
        Setter for the starting year of the activity
        :param new_year:  The year to be set as the new starting year of the activity;
        positive integer >= current, real-life year
        """
        self.start_date_time = self.start_date_time.replace(year=new_year)

    @property
    def end_date_time(self):
        """
        Returns the ending date and time of the activity
        :return: Datetime variable representing the ending date and time of the activity
        """
        return self.__end_date_time

    @end_date_time.setter
    def end_date_time(self, activity_end_date_time):
        """
        Setter for the ending date and time of the activity
        :param activity_end_date_time: Datetime variable to be set as the new activity ending date and time
        """
        self.__end_date_time = activity_end_date_time

    @property
    def end_hour(self):
        """
        Getter for the ending hour of the activity
        :return: The hour at which the activity ends; positive integer in range [0, 23]
         """
        return self.end_date_time.hour

    @end_hour.setter
    def end_hour(self, new_hour):
        """
        Setter for the ending hour of the activity
        :param new_hour: The hour to be set as the new ending hour; positive integer in range [0, 23]
        """
        self.end_date_time = self.end_date_time.replace(hour=new_hour)

    @property
    def end_minute(self):
        """
        Getter for the ending minute of the activity
        :return: The minute at which the activity ends; positive integer in range [0, 59]
        """
        return self.end_date_time.minute

    @end_minute.setter
    def end_minute(self, new_minute):
        """
        Setter for the ending minute of the activity
        :param new_minute: The minute to be set as the new ending minute; positive integer in range [0, 59]
        """
        self.end_date_time = self.end_date_time.replace(minute=new_minute)

    @property
    def end_day(self):
        """
        Getter for the ending day of the activity
        :return: The day when the activity ends; positive integer in range [1, 31]
        """
        return self.end_date_time.day

    @end_day.setter
    def end_day(self, new_day):
        """
        Setter for the ending day of the activity
        :param new_day: The day to be set as the new ending day of the activity; positive integer in range [1, 31]
        """
        self.end_date_time = self.end_date_time.replace(day=new_day)

    @property
    def end_month(self):
        """
        Getter for the ending month of the activity
        :return: The month when the activity ends; positive integer in range [1, 12]
        """
        return self.end_date_time.month

    @end_month.setter
    def end_month(self, new_month):
        """
        Setter for the ending month of the activity
        :param new_month: The month to be set as the new ending month of the activity;
        positive integer in range [1, 12]
        """
        self.end_date_time = self.end_date_time.replace(month=new_month)

    @property
    def end_year(self):
        """
        Getter for the ending year of the activity
        :return: The year when the activity ends; positive integer >= current, real-life year
        """
        return self.end_date_time.year

    @end_year.setter
    def end_year(self, new_year):
        """
        Setter for the ending year of the activity
        :param new_year:  The year to be set as the new ending year of the activity;
        positive integer >= current, real-life year
        """
        self.end_date_time = self.end_date_time.replace(year=new_year)

    @property
    def description(self):
        """
        Getter for the activity description
        """
        return self.__description

    @description.setter
    def description(self, activity_description):
        """
        Setter for the activity description
        :param activity_description: The new activity description
        """
        self.__description = activity_description
