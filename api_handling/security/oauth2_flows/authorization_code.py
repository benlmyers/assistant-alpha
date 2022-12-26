import json

import requests
from flask import Flask, request

app = Flask(__name__)


def authorization_code(flow_data, consumer_key, consumer_secret, scopes):

    print('> Using Authorization Code flow')

    authorization_url = flow_data['authorizationUrl']
    token_url = flow_data['tokenUrl']

    callback_uri = 'http://127.0.0.1:5000/oauth/callback'

    authorization_redirect_url = authorization_url + '?response_type=code&client_id=' + \
        consumer_key + '&redirect_uri=' + \
        callback_uri + '&scope=' + '%20'.join(scopes)

    print("> Open this URL in your browser: " + authorization_redirect_url)
    authorization_code = input('> Enter the code: ')

    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': callback_uri
    }

    print("> Requesting access token")

    access_token_response = requests.post(
        token_url, data=data, verify=False, allow_redirects=False, auth=(consumer_key, consumer_secret))

    tokens = json.loads(access_token_response.text)
    access_token = tokens['access_token']

    return access_token


@app.route("/oauth/callback", methods=["GET"])
def callback():
    print('Callback')
