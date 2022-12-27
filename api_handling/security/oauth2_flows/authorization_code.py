import json
import logging
import os
import signal
import sys
import time
import webbrowser

import requests
from authlib.integrations.requests_client import OAuth2Session
from flask import Flask, redirect, request


def authorization_code(flow_data, client_id, client_secret, scopes):

    app = Flask(__name__)

    log = logging.getLogger('authlib')

    log.addHandler(logging.StreamHandler(sys.stdout))
    log.setLevel(logging.DEBUG)

    print('> Using Authorization Code flow')

    authorization_url = flow_data['authorizationUrl']
    token_url = flow_data['tokenUrl']

    scope = ' '.join(scopes)

    callback_uri = 'http://127.0.0.1:5000/oauth/callback'

    client = OAuth2Session(client_id, client_secret,
                           scope=scope, redirect_uri='REDIRECT')

    uri, state = client.create_authorization_url(
        authorization_url)

    uri = uri.replace('+', '%20')
    uri = uri.replace('REDIRECT', callback_uri)
    uri = uri.replace(
        uri[uri.find('state=') + 6:uri.find('&code_challenge')], 'state')
    uri = uri + '&code_challenge=challenge&code_challenge_method=plain'

    @app.route("/")
    def _():
        return redirect(uri)

    @app.route("/oauth/callback", methods=["GET"])
    def __():
        authorization_response = request.full_path
        token = client.fetch_token(
            token_url, authorization_response=authorization_response, client_secret=client_secret)
        # os.kill(os.getpid(), signal.SIGINT)
        return "Authorized. You can return to the Python app."

    app.run()
