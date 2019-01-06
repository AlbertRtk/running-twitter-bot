# Running Twitter Bot

Bot written in Python 3 tweeting about upcoming running events in Poland.

- Twitter profile of the bot: [Biegi w Polsce](https://twitter.com/biegi_w_pl)
- Source of the information about running events: [maratonypolskie.pl](https://www.maratonypolskie.pl/mp_index.php?dzial=3&action=1&grp=13&trgr=1&bieganie)

### Main Features

- Program creates database, which is updated on Sundays or when it is empty
- Tweeting about events at least eight days in advance
- Tweeting between 8 am and 9 pm, with at least 60 s interval between Tweets

### Requirements

- Installed [Tweepy](https://github.com/tweepy/tweepy)
- Environment variabls or api_kays.py file with Twitter API keys and access tokens

```sh
CONSUMER_KEY = 'your-consumer-key'
CONSUMER_SECRET = 'your-consumer-secret'
ACCESS_TOKEN_KEY = 'your-access-token-key'
ACCESS_TOKEN_SECRET = 'your-access-token-secret'
```