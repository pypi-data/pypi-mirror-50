import requests
import paystacklib
from paystacklib.dictwrapper import DictWrapper
from paystacklib.utils import get_header

class BaseApi:
    def __init__(
            self, secret_key=None,uri='https://api.paystack.co', 
            method=None, headers=None, params=None):
        self.secret_key = paystacklib.secret_key
        self.uri = uri 
        self.method = method
        self.headers = get_header(self.secret_key)
        if not params:
            params = {}
        self.params = {item:params[item] for item in params.keys() if params[item] is not None}

    def execute(self):
        req = getattr(requests, self.method)
        if self.method == 'get':
            result = req(self.uri, headers=self.headers, params=self.params)
        elif self.method == 'post' or self.method == 'put':
            result = req(self.uri, headers=self.headers, json=self.params)
        elif self.method == 'delete':
            result = req(self.uri, headers=self.headers)
        return DictWrapper(result.json())







