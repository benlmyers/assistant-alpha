import json
from authlib.integrations.requests_client import OAuth2Session

import requests
import logging
import sys
from flask import Flask, request

app = Flask(__name__)


def authorization_code(flow_data, client_id, client_secret, scopes):

    log = logging.getLogger('authlib')

    log.addHandler(logging.StreamHandler(sys.stdout))
    log.setLevel(logging.DEBUG)

    print('> Using Authorization Code flow')

    authorization_url = flow_data['authorizationUrl']
    token_url = flow_data['tokenUrl']

    scope = ' '.join(scopes)

    #callback_uri = 'http://127.0.0.1:5000/oauth/callback'
    callback_uri = 'https://www.example.com'

    client = OAuth2Session('Yy1NUVA3RnFKVzFEWWRnZHlINkc6MTpjaQ', client_secret,
                           scope=scope, redirect_uri='REDIRECT')

    uri, state = client.create_authorization_url(
        authorization_url)

    uri = uri.replace('+', '%20')
    uri = uri.replace('REDIRECT', callback_uri)
    uri = uri + '&code_challenge=challenge&code_challenge_method=plain'

    print("> Open this URL in your browser: " + uri)


@app.route("/oauth/callback", methods=["GET"])
def callback():
    print('Callback')
