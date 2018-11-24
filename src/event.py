""" 2018-11-18 by AR
    getevents - scraping of running events info from maratonypolskie.pl
"""
from urllib.request import urlretrieve
from datetime import date
import re


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
    def __init__(self, name, date=None, place=None, distance=None, url=None):
        self.name = name
        self.date = date
        self.place = place
        self.distance = distance
        self.url = url

    def __str__(self):
        return '{} ({}, {}): {}\nURL: {}'.format(self.name, self.place, self.date,
                                              self.distance, self.url)

    def to_dict(self):
        return self.__dict__

    def to_tuple(self):
        return self.name, self.date, self.place, self.distance, self.url


def get_events(year, month, day1, day2):
    """
    :param year: year
    :param month: month
    :param day1: starting day
    :param day2: ending day
    :return: list of instances of class Event with info about events within one
    calendar month from day1 to day2
    """
    print('Getting events from URL')
    url = '{}mp_index.php?dzial=3&action=1&grp=13' \
          '&czasr1={}&czasm1={}&dzienp1={}&dzienk1={}' \
          .format(BASE_URL, year, MONTHS_PL[month], day1, day2)
    print(url)
    filename, headers = urlretrieve(url)

    with open(filename, encoding='iso-8859-2') as f:
        html_code = f.read()

    list_of_events = []

    for day in range(day1, day2+1):
        day_date = '{}.{}.{}'.format(day, month, year)
        date_pattern = '>' + day_date
        date_iter = re.finditer(date_pattern, html_code)

        # Borders to cut out short str (used for data scraping) from HTML code
        spans = []
        for di in date_iter:
            spans.append(di.span()[0])

        for i, span in enumerate(spans):
            # Str (HTML) between two evets dates (last date +500 characters)
            try:
                html_span = html_code[span:spans[i+1]]
            except IndexError:
                html_span = html_code[span:span+500]

            # Scraping info about event
            try:
                place_and_distance = re.search(RE_PLACE_DISTANCE, html_span)
                place_and_distance = place_and_distance.group()
                place, distance = place_and_distance.split('<BR>')

                event_name = re.search(RE_EVENT_NAME, html_span)
                event_name = event_name.group().replace('<BR>', ' ')

                event_url = re.search(RE_URL, html_span).group()
                event_url = BASE_URL + event_url

                list_of_events.append(Event(event_name, day_date, place,
                                            distance, event_url))
            except AttributeError:
                pass

    return list_of_events


if __name__ == '__main__':
    print('Running event.py \n')
    td = date.today()
    y, m, d = td.year, td.month, td.day
    events = get_events(y, m, d, d)

    for e in events:
        print(e)

# EOF
