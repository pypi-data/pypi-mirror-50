from time import time
from urllib.parse import urlparse, parse_qsl, quote
from requests.auth import AuthBase
import novadax.impl.utils as utils

class HTTPAuth(AuthBase):
    _without_content_md5 = ['GET', 'DELETE', 'HEAD']

    def __init__(self, access_key, secret_key):
        self._access_key = access_key
        self._secret_key = secret_key

    def __call__(self, r):
        timestamp = self._get_timestmap()
        sign = self._get_sign(r.method, r.url, r.body, timestamp)
        authorization = '{}:{}:{}'.format(self._access_key, sign, timestamp)
        r.headers['Authorization'] = authorization
        return r

    def _get_timestmap(self):
        return int(time())

    def _get_sign(self, method, url, body, timestamp):
        sign_str = self._get_sign_str(method, url, body, timestamp)
        return utils.hmac_sha1_hex(self._secret_key, sign_str)

    def _get_sign_str(self, method, url, body, timestamp):
        url_parsed = urlparse(url)
        path = url_parsed.path
        params = self._get_sorted_query_params(url_parsed.query)

        if method in self._without_content_md5:
            return '{}\n{}\n{}\n{}'.format(method, path, params, timestamp)

        content_md5 = utils.md5_base64(body.decode('UTF-8'))
        return '{}\n{}\n{}\n{}\n{}'.format(method, path, params, content_md5, timestamp)

    def _get_sorted_query_params(self, query):
        query_dict = dict(parse_qsl(query))
        sorted_query_item = sorted(query_dict.items(), key=lambda x: x[0], reverse=False)
        sorted_query = map(lambda x: '{}={}'.format(quote(x[0]), quote(x[1])), sorted_query_item)
        return '&'.join(sorted_query)
