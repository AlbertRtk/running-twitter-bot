""" 2018 by Albert Ratajczak
    Event - class with info about running event/race + functions
"""
from urllib.request import urlretrieve
from datetime import date, timedelta
from calendar import monthrange
from re import finditer, search
from datetime_functions import date_with_dots


# Webpage to scrape data from
BASE_URL = 'https://www.maratonypolskie.pl/'

MONTHS_PL = {1: 'styczen',
             2: 'luty',
             3: 'marzec',
             4: 'kwiecien',
             5: 'maj',
             6: 'czerwiec',
             7: 'lipiec',
             8: 'sierpien',
             9: 'wrzesien',
             10: 'pazdziernik',
             11: 'listopad',
             12: 'grudzien',
             }

# Patterns used to localize relevant information in HTML code
RE_PLACE_DISTANCE = '[\w\s\.]+<BR>[\w\.,\s]+'
"""
[\w\s\.]+  --> matches name of place including form: Modlin k.Warszawy
[\w\.,\s]+ --> matches numbers with any unut and , or . as decimal separator:
               Eg. 21.1, 42,1 i 50 km
"""

RE_EVENT_NAME = '((<BR>)?[^>]*){1,2}(?=</a>)'
"""
((<BR>)?[^>]*) --> matches 0 or 1 new line <BR> followed by chain of characters
                   except >
{1,2}          --> 1 or 2 repetitions
(?=</a>)       --> matches if is folowed by </a>
                   Eg. Bieg Sylwestrowy</a> or Bieg na <BR> 5 i 10 km</a>
"""

RE_URL = '(?<=href=\')[^\']*'
"""
(?<=href=\')[^\']* --> matches a string of characters after href=' except '
"""


class Event:
    """
    Class with information about events: name, date, place, distance(s) and URL
    """
    def __init__(self, name, date=None, place=None, distance=None, url=None):
        # TODO: TypeErrors
        self.name = name
        self.date = date
        self.place = place
        self.distance = distance
        self.url = url

    def __str__(self):
        return '{} ({}, {}): {}'.format(self.name, self.place,
                                        date_with_dots(self.date),
                                        self.distance)

    def to_dict(self):
        return self.__dict__

    def to_tuple(self):
        return self.name, str(self.date), self.place, self.distance, self.url


def get_events(year, month, day1, day2):
    """
    Scraps info about events between given days in one month (only)

    :param year: year
    :param month: month
    :param day1: starting day
    :param day2: ending day
    :return: list of instances of class Event with info about events within one
    calendar month from day1 to day2
    """
    # Setting URL and downloading HTML code
    url = '{}mp_index.php?dzial=3&action=1&grp=13' \
          '&czasr1={}&czasm1={}&dzienp1={}&dzienk1={}' \
          .format(BASE_URL, year, MONTHS_PL[month], day1, day2)
    print('Getting events from URL: {}'.format(url))
    filename, headers = urlretrieve(url)

    # Reading HTML code
    with open(filename, encoding='iso-8859-2') as f:
        html_code = f.read()

    list_of_events = []

    for day in range(day1, day2+1):
        day_date = date(year, month, day)
        # Info about events is presented on the page in a table
        # First column is date, so we searching for pattern '>dd.mm.yyyy'
        date_pattern = '>' + date_with_dots(day_date)
        # Many events can have the same day, so we use finditer to find all
        date_iter = finditer(date_pattern, html_code)

        # Borders to cut out short str (used for data scraping) from HTML code
        # Each date fitting date_pattern is in first column, so it's new row and
        # info about next event. At the same time each date (except first and
        # last) is endpoint for info about previuos event
        spans = []
        for di in date_iter:
            spans.append(di.span()[0])

        for i, span in enumerate(spans):
            # Str (HTML) between two evets dates (last date +500 characters)
            try:
                html_span = html_code[span:spans[i+1]]
            except IndexError:
                html_span = html_code[span:span+500]

            # Scraping info about event and appending Event instance to list
            try:
                place_and_distance = search(RE_PLACE_DISTANCE, html_span)
                place_and_distance = place_and_distance.group()
                place, distance = place_and_distance.split('<BR>')

                event_name = search(RE_EVENT_NAME, html_span)
                event_name = event_name.group().replace('<BR>', ' ')

                event_url = search(RE_URL, html_span).group()
                event_url = BASE_URL + event_url

                list_of_events.append(Event(event_name, day_date, place,
                                            distance, event_url))
            except AttributeError:
                pass

    return list_of_events


def get_events_2(from_day, days):
    """
    Uses get_events to get info about events from 'from_day' for next 'days'
    days (including 'from_day'). Unlike get_events, get_events_2 is not limited
    to one month. It manages change of month and or year.

    :param from_day: datetime.date instance, begining of time period
    :param days: datetime.date instance, end of time periot
    :return: list of instances of class Event with info about events
    """
    # Days left to search for events (except from_day)
    left_days = days - 1

    # Number of days in month
    month_end = monthrange(from_day.year, from_day.month)[1]

    events = []

    if month_end < from_day.day + left_days:
        # End of callendar month: end of time period in new month
        # till_day (day2 from func get_events) is last day of month
        till_day = date(from_day.year, from_day.month, month_end)
        left_days -= (month_end-from_day.day)
        # Recursion to search events in next month
        events += get_events_2(till_day+timedelta(days=1), left_days)
    else:
        # Time period within one calendar month
        till_day = from_day + timedelta(days=left_days)

    # Calling get_events to search and scrape information
    print('Getting events from {} until {}'.format(from_day, till_day))
    events += get_events(from_day.year, from_day.month,
                         from_day.day, till_day.day)
    return events


if __name__ == '__main__':
    print('Running event.py \n')
    td = date.today()
    y, m, d = td.year, td.month, td.day
    events = get_events(y, m, d, d)

    for e in events:
        print(e)
