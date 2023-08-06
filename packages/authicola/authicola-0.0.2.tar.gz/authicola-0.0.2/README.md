# Authicola
A Python package offering convenient methods for OAuth2.0 authentication

Currently only Google OAuth2.0 has been implemented


Expects a config object passed into the class on instantiation of the Authicola class. 

Scopes are accepted as arguments by the config, but they can also be passed in as a kwarg on the Authicola class method for the driver or a method on the driver itself.

E.g.

```
DRIVERS = {
    'google': {
        'client_id': os.environ.get('GOOGLE_CLIENT'),
        'client_secret': os.environ.get('GOOGLE_SECRET'),
        'redirect_uri': os.environ.get('GOOGLE_REDIRECT'),
        'scopes': ['profile', 'email']
    },
    'github': {
        'client_id': os.environ.get('GITHUB_CLIENT'),
        'client_secret': os.environ.get('GITHUB_SECRET'),
        'redirect_uri': os.environ.get('GITHUB_REDIRECT'),
        'scopes': ['read:user', 'public_repo']
    }
}

a = Authicola(DRIVERS)

# default scope from config used
authorization_url = a.driver('google').redirect_uri()
# https://accounts.google.com/o/oauth2/v2/auth?scope=email+profile&access_type=offline&redirect_uri=<your-redirect-uri>&response_type=code&client_id=<your-client-id>

# only email scope requested as kwarg, overrides config for driver
authorization_url = a.driver('google', scopes=['email']).redirect_uri()
# https://accounts.google.com/o/oauth2/v2/auth?scope=email&access_type=offline&redirect_uri=<your-redirect-uri>&response_type=code&client_id=<your-client-id>

# only profile and email scopes requested manually, this time as method on the driver class, overrides config for driver
authorization_url = a.driver('google').scope('email', 'profile').redirect_uri()
# https://accounts.google.com/o/oauth2/v2/auth?scope=email+profile&access_type=offline&redirect_uri=<your-redirect-uri>&response_type=code&client_id=<your-client-id>

```

On callback from the authentication provider, a params dict is expected for parsing to retrieve the user.

E.g.

```
# callack endpoint

a = Authicola(DRIVERS)

params = request.GET

user = a.driver('google').user(params)
###
{
    'id': <id>,
    'email': 'garyburgmann@gmail.com',
    'verified_email': True,
    'name': 'Gary Burgmann',
    'given_name': 'Gary',
    'family_name': 'Burgmann',
    'picture': '<pic-url>',
    'locale': 'en-GB'
}
###
```
