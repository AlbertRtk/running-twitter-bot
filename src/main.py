""" 2018 by Albert Ratajczak
"""
# General imports
from datetime import date, timedelta
from random import randint
import tweepy

# Local imports
from event import get_events_2
from eventsstorage import EventsStorage
from datetime_functions import date_with_dots, date_of_nearest

# Twitter's APIs keys and tokens
from api_keys import *


# Setting Twitter's APIs
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
twitter = tweepy.API(auth)


# Database to store info about events
storage = EventsStorage('events.db')


tweet_templates = ['{}, {}, dnia {}, dystans: {}\n{}',
                   'Kto biegnie w {}? {}, {}. Dystans: {}\n{}',
                   'Kto startuje w {}? {}, {}. Dystans: {}\n{}',
                   'Forma na {} gotowa? {}, już {} start na: {}\n{}',
                   'Wszyscy na start! {}, {}, dn. {}, {}\n{}',
                   'Do startu! Gotowi! ... {}! {}, start {} na {}\n{}',
                   'A może start w {}? {}, dn. {}. Dystans: {}\n{}'
                   ]


def create_tweet(event):
    tweet = tweet_templates[randint(0, len(tweet_templates)-1)]
    return tweet.format(event.name, event.place, date_with_dots(event.date),
                        event.distance, event.url)


def main():
    # today_day = date(2018, 12, 3)  # for debugging
    today_date = date.today()

    # Updating database with events on Sunday
    if today_date.isoweekday() == 7:
        new_events = get_events_2(today_date+timedelta(days=1), 7)
        storage.store(new_events)

    # Selecting tomorrows events from database
    tweet_events = storage.read(today_date+timedelta(days=1))

    # From Sunday to Thursday selecting also events for nearest weekend
    if today_date.isoweekday() not in (5, 6):
        saturday_events = storage.read(date_of_nearest(day=6))
        sunday_events = storage.read(date_of_nearest(day=7))
        saturday_events = saturday_events[:int(len(saturday_events)/7)]
        sunday_events = sunday_events[:int(len(sunday_events)/7)]
        tweet_events += saturday_events + sunday_events

    # Checking number of Tweets (events) for today
    number_of_teets = len(tweet_events)

    # while today_date == date.today():
    #     pass

    for e in tweet_events:
        tweet = create_tweet(e)
        print('\nTweeting: \n' + tweet)
        # twitter.update_status(tweet)
        # storage.remove(e)


if __name__ == '__main__':
    # while True:
    #     main()
    main()
