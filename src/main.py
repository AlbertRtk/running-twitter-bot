""" 2018 by Albert Ratajczak
"""
# General imports
from datetime import datetime, date, timedelta
from time import sleep
from random import choice
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
    tweet = choice(tweet_templates)
    return tweet.format(event.name, event.place, date_with_dots(event.date),
                        event.distance, event.url)


def main():
    today_date = date.today()
    # today_day = date(2018, 12, 3)  # for debugging

    # On Sunday, updating database with events
    if today_date.isoweekday() == 7:
        new_events = get_events_2(today_date+timedelta(days=1), 7)
        storage.store(new_events)

    # Selecting tomorrows events from database
    events_to_tweet = storage.read(today_date+timedelta(days=1))

    # From Sunday to Thursday selecting also few events for nearest weekend
    if today_date.isoweekday() not in (5, 6):
        saturday_events = storage.read(date_of_nearest(day=6))
        sunday_events = storage.read(date_of_nearest(day=7))
        saturday_events = saturday_events[:int(len(saturday_events)/7)]
        sunday_events = sunday_events[:int(len(sunday_events)/7)]
        events_to_tweet += saturday_events + sunday_events

    # Checking number of Tweets (events) for today
    number_of_teets = len(events_to_tweet)

    # Calculating the time period (in seconds, at least 60 s) between Tweets
    # (assuming that last Tweet will be posted around 8 pm)
    sleep_time = int(3600*(20-datetime.now().time().hour)/number_of_teets)
    if sleep_time < 60: sleep_time = 60
    print('Time interval between Tweets: {}\n'.format(sleep_time))

    while number_of_teets > 0:
        # Creating a Tweet
        tweet_event = choice(events_to_tweet)
        tweet = create_tweet(tweet_event)
        print('='*80)
        print('\n{0:%H}:{0:%M}:{0:%S}, Tweeting:'.format(datetime.now()))
        print(tweet, end='\n'*2)

        # Tweeting
        twitter.update_status(tweet)

        # Removing Tweeted event form the list
        events_to_tweet.remove(tweet_event)
        storage.remove(tweet_event)
        number_of_tweets = len(events_to_tweet)

        if number_of_teets:
            # Waiting sleep_time seconds before posting next Tweet
            next_tweet_time = datetime.now() + timedelta(seconds=sleep_time)
            print('\nTweets to be published: {}.'.format(number_of_teets), end=' ')
            print('Next Tweet at: {0:%H}:{0:%M}:{0:%S}\n'.format(next_tweet_time))
            sleep(sleep_time)


if __name__ == '__main__':
    while True:
        if 9 < datetime.now().hour < 19:
            print('It\' after 9 am, starting Tweeting\n')
            main()
            print('='*80, end='\n'*2)
        else:
            print('Waiting until 9 am')
            sleep(3600)
