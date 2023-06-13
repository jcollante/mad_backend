import os
import threading
import json
import sqlite3

from flask import Flask, request, jsonify, g
from pyngrok import ngrok, conf
# from flask_cors import CORS
from extensions import db, db_a, pd, gpd


os.environ["FLASK_DEBUG"] = "development"

app = Flask(__name__)
# CORS(app)
port = 5000

# set configuration

# ngrok to access the code from an external link
conf.get_default().auth_token = '2NrmZtrypLGk4WtokDp301I3G93_81MTtBkx8R1mLLSB2Sqv1'

if 'COLAB_GPU' in os.environ:
    # Open a ngrok tunnel to the HTTP server
    public_url = ngrok.connect(port).public_url
    print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs to use the public ngrok URL
    app.config["BASE_URL"] = public_url


# ... Update inbound traffic via APIs to use the public-facing ngrok URL
