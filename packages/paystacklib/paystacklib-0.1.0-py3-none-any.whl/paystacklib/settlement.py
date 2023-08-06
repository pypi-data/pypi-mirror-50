
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class Settlement(BaseApi):
    object_type = '/settlement'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)


    @classmethod
    def list(
            cls, fr=None, to=None, subaccount=None): 
        params = copy.deepcopy(locals())
        params['from'] = params['fr'] #from is a keyword in Python
        del params['fr']
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type 
        return cls(uri=uri, method='get', params=params).execute()


