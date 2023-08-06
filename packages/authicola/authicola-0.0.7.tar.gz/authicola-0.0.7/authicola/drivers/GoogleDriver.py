""" The Google Driver Module """
from authicola.settings import DRIVER_CONFIG
from authicola.drivers.BaseDriver import BaseDriver


class GoogleDriver(BaseDriver):
    access_token_url = DRIVER_CONFIG['google']['access_token_url']
    authorization_url = DRIVER_CONFIG['google']['authorization_url']
    profile_url = DRIVER_CONFIG['google']['profile_url']
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
            access_type='offline',
            redirect_uri=self._config['redirect_uri'],
            response_type='code',
            client_id=self._config['client_id']
        )
        return params
