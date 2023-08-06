""" The Google Driver Module """
import json
import urllib

import requests

from authicola.settings import DRIVER_CONFIG


class GoogleDriver:
    access_token_url = DRIVER_CONFIG['google']['access_token_url']
    authorization_url = DRIVER_CONFIG['google']['authorization_url']
    profile_url = DRIVER_CONFIG['google']['profile_url']

    """
    Required: config
    Accepts: scopes
    """
    def __init__(self, config, **kwargs):
        # optionally specify scopes, otherwise default to Authicola config
        self.scopes = kwargs.get('scopes', config.get('scopes'))
        self._config = config

    def redirect_uri(self):
        """ Generate the redirect_uri to Google for client authorization """
        if self.scopes:
            scopes = ' '.join(self.scopes)
        else:
            scopes = ''
        try:
            params = dict(
                scope=scopes,
                access_type='offline',
                redirect_uri=self._config['redirect_uri'],
                response_type='code',
                client_id=self._config['client_id']
            )
            endpoint = \
                '{auth_url}?{params}' \
                .format(
                    auth_url=self.authorization_url,
                    params=urllib.parse.urlencode(params)
                )
        except KeyError as exc:
            raise KeyError(
                'Social auth config for {name} is missing a required key: '
                '{err}'.format(name=__name__, err=str(exc))
            )
        except Exception as exc:
            raise Exception(
                'Error creating redirect_url: {err}'
                .format(err=str(exc))
            )

        return endpoint

    def scope(self, *args):
        """ Set Scopes """
        self.scopes = args
        return self

    def user(self, params):
        """ Try and get the user from the oAuth flow """
        code = params.get('code')
        err = params.get('error')
        # catch returned error param on callback
        if not code and err:
            raise Exception(
                'Authorization failed with error: {err}'
                .format(err=err)
            )
        # catch invalid params argument
        elif not code:
            raise Exception(
                'Authorization code is missing from params: {params}'
                .format(params=str(params))
            )

        try:
            payload = dict(
                code=code,
                grant_type='authorization_code',
                redirect_uri=self._config['redirect_uri'],
                client_id=self._config['client_id'],
                client_secret=self._config['client_secret'],
            )
        except KeyError as exc:
            raise KeyError(
                'Social auth config for {name} is missing a required key: '
                '{err}'.format(name=__name__, err=str(exc))
            )
        except Exception as exc:
            raise Exception(
                'Error creating request body: {err}'
                .format(err=str(exc))
            )

        # Request an access token from the code in the request
        res = requests.post(self.access_token_url, data=payload)
        res.raise_for_status()

        # Get the access token from the response
        try:
            token_response = res.json()
        except ValueError as exc:
            raise ValueError(
                'Error reading token response: {err}'
                .format(str(exc))
            )

        # Exchange the access token for a user
        headers = {
            'Authorization': 'Bearer {}'
            .format(token_response.get('access_token'))
        }

        res = requests.get(self.profile_url, headers=headers)
        res.raise_for_status()

        try:
            return res.json()
        except ValueError as exc:
            raise ValueError(
                'Error reading user response: {err}'
                .format(str(exc))
            )
