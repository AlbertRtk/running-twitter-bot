""" 2018 by Albert Ratajczak
"""
from datetime import date, timedelta
from random import randint
from event import get_events_2
from eventsstorage import EventsStorage
from datetime_functions import date_with_dots


TWEET_TEMPLATE = ['{}, {}, dnia {}, dystans:{}\n{}',
                  'Kto biegnie w {}? {}, {}. Dystans: {}\n{}',
                  'Kto startuje w {}? {}, {}. Dystans: {}\n{}',
                  'Forma na {} gotowa? {}, już {} start na: {}\n{}',
                  'Wszyscy na start! {}, {}, dn. {}, {}\n{}',
                  'Do startu! Gotowi! ... {}! {}, start {} na {}\n{}',
                  'A może start w {}? {}, dn. {}. Dystans: {}\n{}'
                  ]


def create_tweet(event):
    tweet = TWEET_TEMPLATE[randint(0, len(TWEET_TEMPLATE)-1)]
    return tweet.format(event.name, event.place, date_with_dots(event.date),
                        event.distance, event.url)


def main():
    today_date = date.today()
    storage = EventsStorage('events.db')
    todays_events = storage.read(date(2018,12,2))

    if True:  #today_date.isoweekday() == 7:
        new_events = get_events_2(today_date+timedelta(days=1), 7)
        storage.store(new_events)

    for e in todays_events:
        print(create_tweet(e))
        print()
        # storage.remove(e)


if __name__ == '__main__':
    main()
