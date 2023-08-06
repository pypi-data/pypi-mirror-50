import requests
import time
import jwt
from .decoder import (
    decoder_Page,
    decoder_shallowList,
)
from .data import (
    FiatAccount,
    Execution,
)

BASE_URL = 'https://api.liquid.com'

DEFAULT_REQUEST_HEADERS = {
    'X-Quoine-API-Version': '2',
    'Content-Type': 'application/json',
}


class Client(object):
    def __init__(self, baseUrl: str = BASE_URL, apiTokenId: str = '', apiSecret: str = ''):
        self.baseUrl: str = baseUrl
        self.apiTokenId: str = apiTokenId
        self.apiSecret: str = apiSecret
        self.__sess: requests.Session = requests.Session()
        pass

    def __jwt(self, p: str):
        payload = {
            'nonce': int(round(time.time() * 1000)),
            'token_id': self.apiTokenId,
            'path': p,
        }
        return jwt.encode(payload, self.apiSecret, 'HS256')

    def __requestPri(self, method: str, p: str, objectHook: object,
                     params=None, data=None, headers=None, cookies=None, files=None,
                     auth=None, timeout=None, allow_redirects=True, proxies=None, hooks=None,
                     stream=None, verify=None, cert=None, json=None):
        headers['X-Quoine-Auth'] = self.__jwt(p)
        return self.__request(
            method, p, objectHook,
            params, data, headers, cookies, files,
            auth, timeout, allow_redirects, proxies, hooks,
            stream, verify, cert, json,
        )

    def __request(self, method: str, p: str, objectHook: object,
                  params=None, data=None, headers=None, cookies=None, files=None,
                  auth=None, timeout=None, allow_redirects=True, proxies=None, hooks=None,
                  stream=None, verify=None, cert=None, json=None):
        res: requests.Response = self.__sess.request(
            method, '{0}{1}'.format(self.baseUrl, p),
            params, data, headers, cookies, files,
            auth, timeout, allow_redirects, proxies, hooks, stream,
            verify, cert, json,
        )
        res.raise_for_status()
        return res.json(object_hook=objectHook)

    def getExecutions(self, productId: int, limit: int, page: int):
        return self.__request(
            'get', '/executions',
            decoder_Page(Execution),
            params={'product_id': productId, 'limit': limit},
            headers=DEFAULT_REQUEST_HEADERS,
        )

    def getExecutionsByTimestamp(self, productId: int, timestamp: int, limit: int):
        return self.__request(
            'get', '/executions',
            decoder_shallowList(Execution),
            params={'product_id': productId,
                    'limit': limit, 'timestamp': timestamp},
            headers=DEFAULT_REQUEST_HEADERS,
        )

    def getFiatAccounts(self):
        return self.__requestPri(
            'get', '/fiat_accounts',
            decoder_shallowList(FiatAccount),
            headers=DEFAULT_REQUEST_HEADERS,
        )
