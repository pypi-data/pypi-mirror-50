""" The GitHub Driver Module """
from authicola.settings import DRIVER_CONFIG
from authicola.drivers.BaseDriver import BaseDriver


class GitHubDriver(BaseDriver):
    access_token_url = DRIVER_CONFIG['github']['access_token_url']
    authorization_url = DRIVER_CONFIG['github']['authorization_url']
    profile_url = DRIVER_CONFIG['github']['profile_url']
    """
    Required: config
    Accepts: scopes, state
    """
    def __init__(self, config, **kwargs):
        # optionally specify scopes, otherwise default to Authicola config
        super().__init__(config, **kwargs)

    def authorization_params(self, scopes):
        params = dict(
            scope=scopes,
            redirect_uri=self._config['redirect_uri'],
            client_id=self._config['client_id'],
            allow_signup=False
        )
        return params
