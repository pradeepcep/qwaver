from django.test import TestCase

from queries.common.string_formatting import is_int


class ViewTests(TestCase):

	def test_is_int(self):
		assert is_int("") == False
		assert is_int("+me") == False
		assert is_int("example_text") == False
		assert is_int("-50123789") == True
