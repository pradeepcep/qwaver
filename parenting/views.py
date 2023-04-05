from datetime import date, timedelta

from django.shortcuts import render

BRIAN_START = date(2018, 11, 5)


def parenting_calendar(request):
    schedule = []
    for i in range(365):
        the_date = date.today() + timedelta(days=i)
        day = {
            'date': the_date,
            'holiday': get_holiday(the_date),
            'month': the_date.strftime("%B"),
            'pad_days': range(the_date.weekday()),
            'has_kids': has_kids(the_date)
        }
        schedule.append(day)
    return render(request, f'parenting/calendar.html', {'schedule': schedule})


def get_schedule():
    start_date = date.today()
    schedule = []
    for i in range(365):
        today = start_date + timedelta(days=i)
        caretaker = "Kids" if has_kids(today) else "No Kids"
        holiday = get_holiday(today)
        schedule.append(f"{get_string(today)}: {caretaker} {holiday}<br>\n")
    return ''.join(schedule)


def has_kids(day):
    yesterday = day - timedelta(days=1)
    is_even_year = day.year % 2 == 0
    thanks_giving = get_thanksgiving(day.year)
    mothers_day = get_mothers_day(day.year)
    fathers_day = get_fathers_day(day.year)
    christmas_eve = date(day.year, 12, 24)
    christmas = date(day.year, 12, 25)
    memorial_day = get_memorial_day_observed(day.year)
    independence_day = date(day.year, 7, 4)
    labor_day = get_labor_day_observed(day.year)
    if day == thanks_giving:
        return day.year % 2 == 0
    elif day == mothers_day:
        return False
    elif day == fathers_day:
        return True
    elif day == christmas_eve:
        return True
    elif day == christmas:
        return False
    elif day == memorial_day:
        return has_kids(yesterday)
    elif day == labor_day:
        return has_kids(yesterday)
    elif day == independence_day:
        return not is_even_year
    else:
        days_since = (day - BRIAN_START).days
        mod = days_since % 14
        if mod in [0, 1, 4, 5, 6, 9, 10]:
            return True
        else:
            return False


def get_holiday(day):
    year = day.year
    thanks_giving = get_thanksgiving(year)
    mothers_day = get_mothers_day(year)
    fathers_day = get_fathers_day(year)
    christmas_eve = date(year, 12, 24)
    christmas = date(year, 12, 25)
    memorial_day = get_memorial_day_observed(year)
    labor_day = get_labor_day_observed(year)
    daphne_birthday = date(year, 7, 19)
    max_birthday = date(year, 3, 22)
    dash_birthday = date(year, 10, 25)
    lucy_birthday = date(year, 5, 1)
    mom_birthday = date(year, 4, 8)
    kate_birthday = date(year, 5, 4)
    brian_birthday = date(year, 8, 3)
    independence_day = date(year, 7, 4)
    if day == thanks_giving:
        return "Thanksgiving"
    elif day == mothers_day:
        return "Mother's Day"
    elif day == fathers_day:
        return "Father's Day"
    elif day == christmas_eve:
        return "Christmas Eve"
    elif day == christmas:
        return "Christmas"
    elif day == memorial_day:
        return "Memorial Day"
    elif day == labor_day:
        return "Labor Day"
    elif day == independence_day:
        return "4th of July"
    elif day == daphne_birthday:
        return "Daphne's Birthday"
    elif day == max_birthday:
        return "Max's Birthday"
    elif day == dash_birthday:
        return "Dash's Birthday"
    elif day == lucy_birthday:
        return "Lucy's Birthday"
    elif day == mom_birthday:
        return "Mom's Birthday"
    elif day == kate_birthday:
        return "Kate's Birthday"
    elif day == brian_birthday:
        return "Brian's Birthday"
    else:
        return ""


def get_string(day):
    return day.strftime("%Y-%m-%d, %a")


def get_floating_holiday(n_year, month, su, mo, tu, we, th, fr, sa):
    first_day_of_month = date(n_year, month, 1)
    day = first_day_of_month.weekday()
    switcher = {
        6: su,
        0: mo,
        1: tu,
        2: we,
        3: th,
        4: fr,
        5: sa
    }
    holiday_day = switcher.get(day, 0)
    return date(n_year, month, holiday_day)


def get_thanksgiving(n_year):
    return get_floating_holiday(n_year, 11, 26, 25, 24, 23, 22, 28, 27)


def get_mothers_day(n_year):
    return get_floating_holiday(n_year, 5, 8, 14, 13, 12, 11, 10, 9)


def get_fathers_day(n_year):
    return get_floating_holiday(n_year, 6, 15, 21, 20, 19, 18, 17, 16)


def get_memorial_day_observed(n_year):
    n_month = 5
    saved = None
    for day in range(1, 32):
        cal_day = date(n_year, n_month, day)
        if cal_day.weekday() == 0:
            saved = cal_day
    return saved


def get_labor_day_observed(n_year):
    n_month = 9
    saved = None
    for day in range(1, 31):
        cal_day = date(n_year, n_month, day)
        if cal_day.weekday() == 0:
            saved = cal_day
            break
    return saved
