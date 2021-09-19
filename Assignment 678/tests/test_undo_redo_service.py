import unittest

from domain.validators import DateTimeValidator, PersonIDValidator, PhoneNumberValidator
from repository.in_memory_repo import Repository
from repository.undo_redo_repo import RedoRepository, UndoRepository
from services.activity_service import ActivityService
from services.person_service import PersonService
from services.redo_service import RedoService
from services.undo_service import UndoService


class TestUndoRedoService(unittest.TestCase):

    def setUp(self):
        self.activity_repo = Repository()
        self.person_repo = Repository()

        self.datetime_validator_class = DateTimeValidator
        self.persons_id_validator_class = PersonIDValidator
        self.phone_number_validator_class = PhoneNumberValidator

        self.undo_repository = UndoRepository()
        self.redo_repository = RedoRepository()
        self.activity_service = ActivityService(self.activity_repo, self.person_repo, self.datetime_validator_class,
                                                self.persons_id_validator_class, self.undo_repository,
                                                self.redo_repository)
        self.person_service = PersonService(self.person_repo, self.persons_id_validator_class,
                                            self.phone_number_validator_class, self.undo_repository,
                                            self.redo_repository)
        self.person_service.add_person(1, 'Vlad Bogdan', '0745123456')
        self.person_service.add_person(2, 'Test Person', '0258674536')
        self.activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        self.activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        self.double_pop_fns = (self.person_service.add_person, self.activity_service.delete_person_from_activities)
        self.double_pop_fns_counter_part = (self.person_service.delete_person_by_id,
                                            self.activity_service.add_person_to_activities)

        self.undo_service = UndoService(self.undo_repository, self.double_pop_fns, self.double_pop_fns_counter_part)
        self.redo_service = RedoService(self.redo_repository, self.double_pop_fns, self.double_pop_fns_counter_part)

    def test_undo_double_pop(self):
        self.undo_service.record_inverse_operations(self.person_service.delete_person_by_id, 1)
        self.undo_service.record_inverse_operations(self.activity_service.delete_person_from_activities, 1, '1, 2')
        self.undo_service.apply_undo()

    def test_redo_double_pop(self):
        self.redo_service.record_inverse_operations(self.person_service.delete_person_by_id, 1)
        self.redo_service.record_inverse_operations(self.activity_service.delete_person_from_activities, 1, '1, 2')
        self.redo_service.apply_redo()
