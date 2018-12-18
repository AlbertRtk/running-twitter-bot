""" 2018 by Albert Ratajczak
"""
# General imports
from os import getenv
from datetime import datetime, date, timedelta
from time import sleep
from random import choice
from urllib.error import URLError
import tweepy

# Local imports
from event import get_events_2
from eventsstorage import EventsStorage
from datetime_functions import date_with_dots, date_of_nearest

# Twitter's APIs keys and tokens for running on local mashine
# from api_keys import *

# Twitter's credentials for Heroku
CONSUMER_KEY = getenv('CONSUMER_KEY', CONSUMER_KEY_LOCAL)
CONSUMER_SECRET = getenv('CONSUMER_SECRET', CONSUMER_SECRET_LOCAL)
ACCESS_TOKEN_KEY = getenv('ACCESS_TOKEN_KEY', ACCESS_TOKEN_KEY_LOCAL)
ACCESS_TOKEN_SECRET = getenv('ACCESS_TOKEN_SECRET', ACCESS_TOKEN_SECRET_LOCAL)


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

    # Table is empty or it's Sunday, updating database with events
    if storage.count() == 0 or today_date.isoweekday() == 7:
        update = 0
        while update < 5:
            try:
                new_events = get_events_2(today_date+timedelta(days=8), 7)
                storage.store(new_events)
                break
            except URLError:
                print('URLError: URL is not available! Waiting one hour')
                update += 1
                sleep(3600)

    # Selecting from database events which are in 8 days
    events_to_tweet = storage.read(today_date+timedelta(days=8))

    # From Sunday to Thursday selecting also few events for next weekend
    if today_date.isoweekday() not in (5, 6):
        saturday_events = storage.read(date_of_nearest(day=6)+timedelta(days=7))
        sunday_events = storage.read(date_of_nearest(day=7)+timedelta(days=7))
        saturday_events = saturday_events[:int(len(saturday_events)/7)]
        sunday_events = sunday_events[:int(len(sunday_events)/7)]
        events_to_tweet += saturday_events + sunday_events

    # Checking number of Tweets (events) for today
    number_of_tweets = len(events_to_tweet)

    if number_of_tweets:
        # Calculating the time period (in seconds, at least 60 s) between Tweets
        # (assuming that last Tweet will be posted around 8-9 pm)
        sleep_time = int(3600*(21-datetime.now().time().hour)/number_of_tweets)
        if sleep_time < 60: sleep_time = 60
        print('Time interval between Tweets: {}\n'.format(sleep_time))
    else:
        print('No Tweet to be published')
        return False

    while number_of_tweets:
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

        if number_of_tweets:
            # Waiting sleep_time seconds before posting next Tweet
            next_tweet_time = datetime.now() + timedelta(seconds=sleep_time)
            print('\nTweets to be published: {}.'.format(number_of_tweets), end=' ')
            print('Next Tweet at: {0:%H}:{0:%M}:{0:%S}\n'.format(next_tweet_time))
            sleep(sleep_time)


if __name__ == '__main__':
    print('Starting bot\n')
    awaiting_tweets = True
    while True:
        if 8 < datetime.now().hour < 21 and awaiting_tweets:
            print('It\'s after 8 am, starting Tweeting\n')
            main()
            awaiting_tweets = False
            print('\n'+'='*80, end='\n'*2)
        else:
            if datetime.now().hour > 20: awaiting_tweets = True
            print('Waiting until 8 am')
            sleep(3600)  # 1h
