""" The Base Driver Module """
import json
import urllib

import requests


class BaseDriver:
    """
    Required: config
    Accepts: scopes, state
    """
    def __init__(self, config, **kwargs):
        # optionally specify scopes, otherwise default to Authicola config
        self._scopes = kwargs.get('scopes', config.get('scopes'))
        self._state = kwargs.get('state')
        self._config = config

    def authorization_params(self, scopes):
        raise NotImplementedError(
            'authorization_params method has not been implemented'
        )

    def token_params(self, code):
        payload = dict(
            code=code,
            grant_type='authorization_code',
            redirect_uri=self._config['redirect_uri'],
            client_id=self._config['client_id'],
            client_secret=self._config['client_secret'],
        )
        return payload

    def redirect_uri(self):
        """ Generate the redirect_uri for client authorization """
        if self.scopes:
            scopes = ' '.join(self._scopes)
        else:
            scopes = ''
        try:
            params = self.authorization_params(scopes)
            if self._state:
                params.update(state=self._state)
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

    def scopes(self, *args):
        """ Set Scopes """
        self._scopes = args
        return self

    def state(self, state):
        """ Set state """
        if not isinstance(state, str):
            raise Exception('state param must be a string')
        self._state = state
        return self

    """
    Required: params
    Accepts: state
    """
    def user(self, params, state=None):
        """ Try and get the user from the oAuth flow """
        code = params.get('code')
        err = params.get('error')
        state_param = params.get('state')

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

        if state and state != state_param:
            raise Exception(
                'Invalid state parameter detected'
            )

        try:
            payload = self.token_params(code)
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
        headers = {
            'Accept': 'application/json'
        }
        res = requests.post(
            self.access_token_url,
            headers=headers,
            data=payload
        )
        res.raise_for_status()

        # Get the access token from the response
        try:
            token_response = res.json()
        except ValueError as exc:
            raise ValueError(
                'Error reading token response: {err}\n{data}'
                .format(err=str(exc), data=res.text)
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
