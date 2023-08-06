""" Authicola root class """
# from config import authicola
from authicola.drivers import (
    GoogleDriver,
    GitHubDriver
)


class Authicola:
    """
    Required: config
    """
    def __init__(self, config):
        self.config = config

    """
    Required: name
    Accepts: scopes
    """
    def driver(self, name, **kwargs):
        try:
            chosen_driver = None
            if name == 'google':
                chosen_driver = GoogleDriver
            elif name == 'github':
                chosen_driver = GitHubDriver
            if chosen_driver:
                return chosen_driver(
                    config=self.config[name],
                    **kwargs
                )
        except KeyError:
            raise KeyError(
                'Config for driver "{driver}" not found'
                .format(driver=name)
            )
        except Exception as exc:
            raise KeyError(
                'Error loading driver "{driver}": {err}'
                .format(driver=name, err=str(exc))
            )
        
        raise NotImplementedError(
            'Social driver "{driver}" not found'
            .format(driver=name)
        )
