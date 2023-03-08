from django.test import TestCase

from queries.common.string_formatting import is_float


class ViewTests(TestCase):

	def test_is_float(self):
		assert is_float("7.3") == True
		assert is_float("50123789") == True
		assert is_float("example_text") == False
		assert is_float("+^-") == False
