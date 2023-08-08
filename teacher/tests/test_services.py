from unittest import TestCase

from teacher.models import Classroom
from teacher.services.models_services import get_random_string
from teacher.services.set_context import set_context


class SetContextTestCase(TestCase):

    def test_set_context(self) -> None:
        """Checks if custom set_context function return a dict with received values."""
        self.assertDictEqual(set_context({}, pk=1, student=2), {'pk': 1, 'student': 2})
