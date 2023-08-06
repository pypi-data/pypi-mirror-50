import requests
from novadax.impl.http_auth import HTTPAuth

class HTTPClient(object):
    def __init__(self, url, access_key, secret_key):
        self._url = url
        self._auth = HTTPAuth(access_key, secret_key)

    def get(self, path, params = dict()):
        return self._request(False, 'get', path, params = params)

    def post(self, path, params = dict(), json = dict()):
        return self._request(False, 'post', path, params = params, json = json)

    def get_with_auth(self, path, params = dict()):
        return self._request(True, 'get', path, params = params)

    def post_with_auth(self, path, params = dict(), json = dict()):
        return self._request(True, 'post', path, params = params, json = json)

    def _request(self, auth, method, path, **kwargs):
        url = self._url + path
        if auth:
            kwargs['auth'] = self._auth

        if 'params' in kwargs:
            if kwargs['params'] is None:
                del kwargs['params']
            else:
                kwargs['params'] = self._filter_none(kwargs['params'])

        if 'json' in kwargs:
            if kwargs['json'] is None:
                del kwargs['json']
            else:
                kwargs['json'] = self._filter_none(kwargs['json'])

        if 'timeout' not in kwargs:
            kwargs['timeout'] = 30

        r = requests.request(method, url, **kwargs)
        return r.json()

    def _filter_none(self, data):
        if isinstance(data, dict):
            return { k: v for k,v in data.items() if v is not None }
        return data