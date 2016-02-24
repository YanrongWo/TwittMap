####################################################################
# data_pipeline/__init__.py
# COMS E6998, Assignment 1 - TwittMap
# 
# Performs and reads necessary configuration files required to
# gather tweet data.
#
# Dependencies: twitter, elasticsearch
####################################################################

import os
import sys
import json

if os.environ.get("TWITTMAP_CONFIGURED") == None:
	with open(os.path.dirname(os.path.realpath(__file__))+"/../config.json", 'r') as f:
		config = json.loads(f.read())

		os.environ["TWITTMAP_ES_NODES"] = json.dumps(config["elasticsearch"]["nodes"])
		os.environ["TWITTMAP_TWITTER_CONSUMER_KEY"] = config["twitter"]["consumer_key"]
		os.environ["TWITTMAP_TWITTER_CONSUMER_SECRET"] = config["twitter"]["consumer_secret"]
		os.environ["TWITTMAP_TWITTER_ACCESS_TOKEN"] = config["twitter"]["access_token"]
		os.environ["TWITTMAP_TWITTER_ACCESS_TOKEN_SECRET"] = config["twitter"]["access_token_secret"]

		os.environ["TWITTMAP_CONFIGURED"] = "1"

if os.environ.get("TWITTMAP_CONFIGURED") == None:
	print "Invalid or missing configuration."
	sys.exit(1)

