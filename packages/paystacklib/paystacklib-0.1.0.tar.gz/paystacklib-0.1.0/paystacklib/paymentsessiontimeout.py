
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class PaymentSessionTimeout(BaseApi):
    object_type = '/payment_session_timeout'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)


    @classmethod
    def fetch(cls):
        uri = paystacklib.api_base + \
            '/integration{0}'.format(cls.object_type)
        return cls(uri=uri, method='get').execute()

    @classmethod    
    def update(cls, timeout):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + \
            '/integration{0}'.format(cls.object_type)
        return cls(uri=uri, method='put', params=params).execute()


