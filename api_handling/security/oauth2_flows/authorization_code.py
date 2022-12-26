import json
from authlib.integrations.requests_client import OAuth2Session

import requests
from flask import Flask, request

app = Flask(__name__)


def authorization_code(flow_data, consumer_key, consumer_secret, scopes):

    print('> Using Authorization Code flow')

    authorization_url = flow_data['authorizationUrl']
    token_url = flow_data['tokenUrl']

    scope = ' '.join(scopes)

    callback_uri = 'http://127.0.0.1:5000/oauth/callback'

    client = OAuth2Session(consumer_key, consumer_secret,
                           scope=scope, redirect_uri=callback_uri)

    uri, state = client.create_authorization_url(authorization_url)

    print("> Open this URL in your browser: " + uri)


@app.route("/oauth/callback", methods=["GET"])
def callback():
    print('Callback')
