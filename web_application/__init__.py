####################################################################
# web_application/__init__.py
# COMS E6998, Assignment 1 - TwittMap
# 
# Performs and reads necessary configuration files required to
# gather query tweet data.
#
# Dependencies: twitter, elasticsearch
####################################################################

import os
import sys
import json

if os.environ.get("TWITTMAP_WEB_CONFIGURED") == None:
	with open(os.path.dirname(os.path.realpath(__file__))+"/../config.json", 'r') as f:
		config = json.loads(f.read())

		os.environ["TWITTMAP_ES_NODES"] = json.dumps(config["elasticsearch"]["nodes"])

		os.environ["TWITTMAP_WEB_CONFIGURED"] = "1"

if os.environ.get("TWITTMAP_WEB_CONFIGURED") == None:
	print "Invalid or missing configuration."
	sys.exit(1)
