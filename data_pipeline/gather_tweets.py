####################################################################
# gather_tweets.py
# COMS E6998, Assignment 1 - TwittMap
# 
# Streams tweets from the Twitter 'hose,' storing them in the 
# configured elasticsearch cluster.
#
# Dependencies: twitter, elasticsearch
####################################################################

from __init__ import *  # Ensure proper fields have been configured

import os

import json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from elasticsearch import Elasticsearch


es = Elasticsearch(json.loads(os.environ["TWITTMAP_ES_NODES"]) \
	if os.environ["TWITTMAP_ES_NODES"] != None else None)

consumer_key = os.environ["TWITTMAP_TWITTER_CONSUMER_KEY"]
consumer_secret = os.environ["TWITTMAP_TWITTER_CONSUMER_SECRET"]

access_token = os.environ["TWITTMAP_TWITTER_ACCESS_TOKEN"]
access_token_secret = os.environ["TWITTMAP_TWITTER_ACCESS_TOKEN_SECRET"]

oauth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret)

twitter_stream = TwitterStream(auth=oauth)

cursor = twitter_stream.statuses.sample()

print "Indexing tweets..."
for tweet in cursor:
	try: 
		if tweet["coordinates"] != None:
			es.index(index='tweet', doc_type='tweet', body=tweet)
		else:
			pass # No coordinates
	except KeyError, e:
		pass # No coordinates

print "Tweets indexed."