from django.test import TestCase

from queries.common.string_formatting import is_date


class ViewTests(TestCase):

	def test_is_date(self):
		assert is_date("2005-10-05") == True
		assert is_date("1554-11-07") == True
		assert is_date("a2005-10-05") == False
		assert is_date("example_text") == False
		assert is_date("%2005-10-05^") == False
