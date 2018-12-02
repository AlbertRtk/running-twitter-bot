""" 2018 by Albert Ratajczak
"""
from datetime import date, timedelta


def date_of_nearest(day):
    """
    :param day: day of week as int - Monday = 1 ... Sunday = 7
    :return: date of next nearest day
    """
    # today_day = date(2018, 12, 3)  # for debugging
    today = date.today()
    today_day = today.isoweekday()
    if today_day == day:
        days = 7
    elif today_day < day:
        days = day - today_day
    else:  # today_day > day
        days= 7 + day - today_day
    return today + timedelta(days=days)


def date_with_dots(date_obj):
    """
    :param date_object: date to convert to a starting
    :return: string with date in form 'd.m.Y' - long year (eg. 2018),
    no zero prefix in day and month, eg. 1.1.2018, 18.2.2018, 1.11.2018)
    """
    return '{}.{}.{}'.format(date_obj.day, date_obj.month, date_obj.year)
