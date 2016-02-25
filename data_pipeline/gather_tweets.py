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

# create geospatial mapping
try:
	es.indices.create(index='tweet', ignore=400)
	mapping = {"tweet": { "properties": { "coordinates": {"properties": { "coordinates": { "type": "geo_point" }, "type": {"type": "string"}}}}}}
	es.indices.put_mapping(index='tweet',doc_type='tweet',body=mapping)
except Exception, e:
	pass
 
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
			print "[i] Tweet indexed"
			es.index(index='tweet', doc_type='tweet', body=tweet)
		else:
			pass # No coordinates
	except KeyError, e:
		pass # No coordinates

print "Tweets indexed."