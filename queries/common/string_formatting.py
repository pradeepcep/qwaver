import re
import datetime


def sanitize_name(string):
    string = string.lower()
    string = re.sub(r'[^\w\s]', '', string)
    string = re.sub(r'[\s]', '_', string)
    return string


def is_int(s):
    if len(s) == 0:
        return False
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def is_float(element: any) -> bool:
    # If you expect None to be passed:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


# checks for format YYYY-MM-DD
def is_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False