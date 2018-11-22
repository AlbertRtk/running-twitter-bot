from datetime import date
from event import get_events
from eventsstorage import EventsStorage


if __name__ == '__main__':
    td = date.today()
    y, m, d = td.year, td.month, td.day
    events = get_events(y, m, d, d)

    for e in events:
        print(e)

    storage = EventsStorage('events.db')
    storage.store(  events)

    events2 = storage.read()
    for e in events2:
        print(e)

    event_name = events2[0].name
    storage.remove(event_name)

    events2 = storage.read()
    for e in events2:
        print(e)
