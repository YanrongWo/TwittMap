####################################################################
# web_application/server.py
# COMS E6998, Assignment 1 - TwittMap
# 
# Performs routing for the TwittMap web application.
#
# Dependencies: elasticsearch
####################################################################

from __init__ import * # Ensure proper configuration is in place for querying tweets

from flask import Flask, request, render_template, g, redirect, Response, make_response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)