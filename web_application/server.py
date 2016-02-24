####################################################################
# web_application/server.py
# COMS E6998, Assignment 1 - TwittMap
# 
# Performs routing for the TwittMap web application.
#
# Dependencies: elasticsearch
####################################################################

from __init__ import * # Ensure proper configuration is in place for querying tweets

from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, g, redirect, Response, make_response, jsonify
import os
import sys

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

@app.route('/', methods=["POST", "GET"])
def index():
	return render_template("index.html")

@app.route('/search', methods=['GET'])
def search():
	keyword = request.args.get('keyword')
	if keyword == None:
		return "{\"results\": []}"
	else:
		es = Elasticsearch(json.loads(os.environ["TWITTMAP_ES_NODES"]) \
			if os.environ["TWITTMAP_ES_NODES"] != None else None)
		query_body = { "query": { "match": { "text": { "query": keyword, "operator": "or" } } } }
		results = es.search(index='tweet', body=query_body)
		return jsonify( { "results": results["hits"]["hits"] } )


if __name__ == "__main__":
	host, port = "0.0.0.0", 8000
	if len(sys.argv) >= 3:
		host = sys.argv[1]
		port = sys.argv[2]

	app.run(host=host, port=port, debug=True)

	run()
