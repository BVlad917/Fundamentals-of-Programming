import datetime
import unittest

from domain.activity import Activity


class TestActivity(unittest.TestCase):

    def setUp(self):
        act1_dt1 = datetime.datetime(2021, 5, 17, 17, 30)
        act1_dt2 = datetime.datetime(2021, 5, 17, 19, 0)
        act2_dt1 = datetime.datetime(2021, 6, 17, 19, 30)
        act2_dt2 = datetime.datetime(2021, 6, 17, 21, 0)
        self.activity_1 = Activity(1, act1_dt1, act1_dt2, 'birthday', [1, 2, 3])
        self.activity_2 = Activity(2, act2_dt1, act2_dt2, 'swimming', [1, 2, 3, 4])

    def test_str(self):
        act3_dt1 = datetime.datetime(2021, 5, 17, 17, 30)
        act3_dt2 = datetime.datetime(2021, 5, 18, 16, 45)
        activity3 = Activity(3, act3_dt1, act3_dt2, 'fun')
        expected_str_act1 = f"Activity ID 1\n" \
                            f"\tDescription of the activity: birthday\n" \
                            f"\tIDs of the persons signed up for this activity: 1, 2, 3\n" \
                            f"\tDate of the activity: 2021/5/17\n" \
                            f"\tTime interval of the activity: 17:30 - 19:00"
        self.assertEqual(str(self.activity_1), expected_str_act1)

        expected_str_act3 = f"Activity ID 3\n" \
                            f"\tDescription of the activity: fun\n" \
                            f"\tIDs of the persons signed up for this activity: \n" \
                            f"\tTime interval of the activity: 2021/05/17 17:30 - 2021/05/18 16:45"
        self.assertEqual(str(activity3), expected_str_act3)

    def test_repr(self):
        expected_act1_repr = "Activity ID: 1; Person IDs: [1, 2, 3]; Start time: 2021-05-17 17:30:00;" \
                             "End time: 2021-05-17 19:00:00; Description: birthday"
        self.assertEqual(repr(self.activity_1), expected_act1_repr)

    def test_setters(self):
        self.activity_1.start_hour = 10
        self.assertEqual(self.activity_1.start_hour, 10)
        self.activity_1.start_minute = 20
        self.assertEqual(self.activity_1.start_minute, 20)
        self.activity_1.start_year = 2010
        self.assertEqual(self.activity_1.start_year, 2010)
        self.activity_1.start_month = 5
        self.assertEqual(self.activity_1.start_month, 5)
        self.activity_1.start_day = 17
        self.assertEqual(self.activity_1.start_day, 17)

        self.activity_1.end_hour = 11
        self.assertEqual(self.activity_1.end_hour, 11)
        self.activity_1.end_minute = 20
        self.assertEqual(self.activity_1.end_minute, 20)
        self.activity_1.end_year = 2010
        self.assertEqual(self.activity_1.end_year, 2010)
        self.activity_1.end_month = 5
        self.assertEqual(self.activity_1.end_month, 5)
        self.activity_1.end_day = 17
        self.assertEqual(self.activity_1.end_day, 17)

    def test_activity_eq(self):
        new_act_dt1 = datetime.datetime(2021, 5, 17, 17, 30)
        new_act_dt2 = datetime.datetime(2021, 5, 17, 19, 0)
        new_activity = Activity(1, new_act_dt1, new_act_dt2, 'birthday', [1, 2, 3])
        self.assertTrue(new_activity == self.activity_1)
        self.assertFalse(new_activity == self.activity_2)

    def test_get_all_person_ids_in_activity(self):
        self.assertEqual(self.activity_1.get_all_person_ids_in_activity(), [1, 2, 3])
        self.assertEqual(self.activity_2.get_all_person_ids_in_activity(), [1, 2, 3, 4])

    def test_add_person_id(self):
        self.activity_1.add_person_id(4)
        self.assertEqual(self.activity_1.get_all_person_ids_in_activity(), [1, 2, 3, 4])
        self.activity_1.add_person_id(4)
        self.assertEqual(self.activity_1.get_all_person_ids_in_activity(), [1, 2, 3, 4, 4])

    def test_remove_person_id(self):
        self.activity_1.remove_person_id(3)
        self.assertEqual(self.activity_1.get_all_person_ids_in_activity(), [1, 2])
        self.assertRaises(ValueError, self.activity_1.remove_person_id, 3)

    def test_change_start_and_end_date(self):
        dt = datetime.datetime(2021, 5, 17, 17, 30)
        self.assertEqual(self.activity_1.start_date_time, dt)

        dt = datetime.datetime(2021, 5, 19, 21, 0)
        self.activity_1.change_start_date(dt)
        self.assertEqual(self.activity_1.start_date_time, dt)

        dt = datetime.datetime(2021, 5, 20, 1, 0)
        self.activity_1.change_end_date(dt)
        self.assertEqual(self.activity_1.end_date_time, dt)

    def test_change_description(self):
        self.activity_1.change_description("Football")
        self.assertEqual(self.activity_1.description, 'Football')
