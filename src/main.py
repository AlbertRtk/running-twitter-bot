""" 2018 by Albert Ratajczak
"""
from datetime import date, timedelta
from event import get_events, get_events_2
from eventsstorage import EventsStorage


def main():
    today_date = date.today()
    storage = EventsStorage('events.db')
    todays_events = storage.read(date(2018,12,2))

    # if True:  #today_date.isoweekday() == 7:
    #     new_events = get_events_2(today_date+timedelta(days=1), 7)
    #     storage.store(new_events)

    for e in todays_events:
        print(e)
        storage.remove(e)


if __name__ == '__main__':
    main()
