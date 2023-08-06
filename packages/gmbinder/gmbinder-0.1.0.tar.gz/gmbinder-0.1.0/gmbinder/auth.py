import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r


class BinderAuth(requests.auth.AuthBase):
    def __init__(self, username, password, *, host):
        self.credentials = (username, password)
        self.host = host

    @property
    def endpoint(self):
        return f'{self.host}/oauth/token'

    # Tempting to memoize this call but endpoint doesn't return a TTL and
    # making a request to "test" if token is still valid is just as expensive
    # as re-requesting a token that happens to be the same
    def request_token(self):
        r = requests.get(
                self.endpoint,
                auth=self.credentials
        )
        return r.json()['token']

    def __call__(self, r):
        return BearerAuth(self.request_token())(r)
        return r