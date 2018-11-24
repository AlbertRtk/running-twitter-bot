from datetime import date, timedelta
from calendar import monthrange
from event import get_events
from eventsstorage import EventsStorage


def test():
    td = date.today()
    y, m, d = td.year, td.month, td.day
    events = get_events(y, m, d, d)

    for e in events:
        print(e)

    storage = EventsStorage('events.db')
    storage.store(events)

    events2 = storage.read()
    for e in events2:
        print(e)

    event_name = events2[0].name
    storage.remove(event_name)

    events2 = storage.read()
    for e in events2:
        print(e)


if __name__ == '__main__':
    today_date = date.today()
    month_end = monthrange(today_date.year, today_date.month)[1]

    if today_date.isoweekday() == 6 or today_date.day == month_end:
        from_day = today_date + timedelta(days=1)

        if month_end < from_day.day+7:
            till_day = date(from_day.year, from_day.month, month_end)
        else:
            till_day = td + timedelta(days=7)

        print(from_day, till_day)

        events = get_events(from_day.year, from_day.month, from_day.day, till_day.day)
