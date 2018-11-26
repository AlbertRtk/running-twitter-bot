""" 2018 by Albert Ratajczak
"""
from datetime import date


def date_of_nearest(day):
    """
    :param day: day of week as int - Monday = 1 ... Sunday = 7
    :return: date of nearest day
    """
    today = date.today()
    return today + timedelta(days=day-today.isoweekday())


def date_with_dots(date_obj):
    """
    :param date_object: date to convert to a starting
    :return: string with date in form 'd.m.Y' - long year (eg. 2018),
    no zero prefix in day and month, eg. 1.1.2018, 18.2.2018, 1.11.2018)
    """
    return '{}.{}.{}'.format(date_obj.day, date_obj.month, date_obj.year)
