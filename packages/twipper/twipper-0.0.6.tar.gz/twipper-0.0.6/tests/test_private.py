#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Alvaro Bartolome @ alvarob96 on GitHub'
__version__ = '0.0.6'

from twipper.streaming import stream_country_tweets
from twipper.credentials import TwipperCredentials


credentials = TwipperCredentials(consumer_key='4mfeYj9SH1PXsff5HgZ5bTOzW',
                                 consumer_secret='aiEfkE5tYCKcKEg42OcHbNgVvA2uikwwpRuBYwl5VmGSAm7N7e',
                                 access_token='254490342-xIGPeyGYLDyD1uFIVgybDsd9ImUPaz467kowIoem',
                                 access_token_secret='JrEuYnm1s44JR46AQDdoJagee3Uw9Ip0jxlp7z3XFcPDg')

api = credentials.get_api()

tweets = stream_country_tweets(auth=credentials.get_oauth(),
                               country='spain',
                               language='es',
                               filter_retweets=False,
                               tweet_limit=10,
                               retry='no_limit')  # after cleaning maybe some are empty or invalid

credentials.invalidate_oauth_token()

for tweet in tweets:
    print(tweet)