####################################################################
# web_applicationlication/server.py
# COMS E6998, Assignment 1 - TwittMap
# 
# Performs routing for the TwittMap web applicationlication.
#
# Dependencies: elasticsearch
####################################################################

from __init__ import * # Ensure proper configuration is in place for querying tweets

from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, g, redirect, Response, make_response, jsonify
import os
import sys

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
application = Flask(__name__, template_folder=tmpl_dir)


# Home Page
@application.route('/', methods=["POST", "GET"])
def index():
	return render_template("index.html")

# Get results to a tag search
@application.route('/search', methods=['GET'])
def search():
	keyword = request.args.get('keyword')
	if keyword == None:
		return jsonify({"results": []})
	else:
		es = Elasticsearch(json.loads(os.environ["TWITTMAP_ES_NODES"]) \
			if os.environ["TWITTMAP_ES_NODES"] != None else None)
		query_body = { "query": { "match": { "text": { "query": keyword, "operator": "or" } } } }
		results = es.search(index='tweet', body=query_body)
		return jsonify( { "results": results["hits"]["hits"] } )

# Get results to a map radius search
@application.route('/within_radius', methods=['GET'])
def within_radius():
	lat = request.args.get('lat')
	lon = request.args.get('lon')

	try:
		lat, lon = float(lat), float(lon)
	except ValueError, e:
		return jsonify({"results": []})

	if lat == None or lon == None:
		return jsonify({"results": []})
	else:
		es = Elasticsearch(json.loads(os.environ["TWITTMAP_ES_NODES"]) \
			if os.environ["TWITTMAP_ES_NODES"] != None else None)

		query_body= {"query":{"filtered":{"query":{"match_all":{}},"filter" : {"geo_distance" : {"distance" : "500km","coordinates.coordinates" : {"lat" : lat,"lon" : lon}}}}}}

		results = es.search(index='tweet', body=query_body)
		return jsonify( {"results": results["hits"]["hits"]} )

# Main function
if __name__ == "__main__":
	host, port = "0.0.0.0", 5000
	if len(sys.argv) >= 3:
		host = sys.argv[1]
		port = sys.argv[2]

	application.run(host=host, port=port, debug=True)

	run()
