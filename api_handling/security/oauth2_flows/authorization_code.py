import json
import logging
import os
import signal
import sys
import time

import requests
from authlib.integrations.requests_client import OAuth2Session
from waiting import wait

access_token = ''


def authorization_code(flow_data, client_id, client_secret, scopes):

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

    print('Open this URL in your browser: ' + uri)

    callback = input('Paste the URL here: ')

    code = callback[callback.find('code=') + 5:]

    resp = requests.post(
        token_url,
        data={
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'redirect_uri': callback_uri,
            'code_verifier': 'challenge'
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic WXkxTlVWQTNSbkZLVnpGRVdXUm5aSGxJTmtjNk1UcGphUTpzaGd6MFFjWU56MjVmT3VXcmxGVmZaUTFQWW9nTlN0Z1VVTlpTY0lleUQycHgySFBDdA=='
        }
    )

    access_token = resp.json()['access_token']

    print('> Authorized.')

    return access_token


def test():
    authorization_code(
        {
            "authorizationUrl": "https://twitter.com/i/oauth2/authorize",
            "tokenUrl": "https://api.twitter.com/2/oauth2/token",
        },
        "Yy1NUVA3RnFKVzFEWWRnZHlINkc6MTpjaQ",
        "shgz0QcYNz25fOuWrlFVfZQ1PYogNStgUUNZScIeyD2px2HPCt",
        ['tweet.read', 'tweet.write', 'users.read']
    )
