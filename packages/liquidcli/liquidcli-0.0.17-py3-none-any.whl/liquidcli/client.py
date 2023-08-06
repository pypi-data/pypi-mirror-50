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
    def __init__(self, baseUrl: str = BASE_URL, apiTokenId: str = '', apiSecret: str = '', noncer=lambda: int(round(time.time() * 1000))):
        self.baseUrl: str = baseUrl
        self.apiTokenId: str = apiTokenId
        self.apiSecret: str = apiSecret
        self.__sess: requests.Session = requests.Session()
        self.noncer = noncer

    def __jwt(self, p: str):
        payload = {
            'nonce': self.noncer(),
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
            params=params, data=data, headers=headers, cookies=cookies, files=files,
            auth=auth, timeout=timeout, allow_redirects=allow_redirects,
            proxies=proxies, hooks=hooks, stream=stream,
            verify=verify, cert=cert, json=json,
        )
        res.raise_for_status()
        return res.json(object_hook=objectHook)

    def getExecutions(self, productId: int, limit: int, page: int):
        return self.__request(
            'get', '/executions',
            decoder_Page(Execution),
            params={'product_id': productId, 'limit': limit, 'page': page},
            headers=DEFAULT_REQUEST_HEADERS,
        )

    def getExecutionsByTimestamp(self, currencyPairCode: str, timestamp: int, limit: int):
        return self.__request(
            'get', '/executions',
            decoder_shallowList(Execution),
            params={'currency_pair_code': currencyPairCode,
                    'limit': limit, 'timestamp': timestamp},
            headers=DEFAULT_REQUEST_HEADERS,
        )

    def getFiatAccounts(self):
        return self.__requestPri(
            'get', '/fiat_accounts',
            decoder_shallowList(FiatAccount),
            headers=DEFAULT_REQUEST_HEADERS,
        )
