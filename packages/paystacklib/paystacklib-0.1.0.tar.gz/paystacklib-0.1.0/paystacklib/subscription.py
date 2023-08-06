
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class Subscription(BaseApi):
    object_type = '/subscription'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)

    @classmethod
    def create(cls, customer, plan, authorization, start_date=None):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type
        return cls(uri=uri, method='post', params=params).execute() 


    @classmethod
    def list(
            cls, per_page=50, page=1, customer=None, plan=None): 
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type 
        return cls(uri=uri, method='get', params=params).execute()

    @classmethod
    def disable(cls, code, token):
        params = copy.deepcopy(locals())
        uri = paystacklib.api_base + cls.object_type + '/disable'
        return cls(uri=uri, method='post', params=params)

    @classmethod
    def enable(cls, code, token):
        params = copy.deepcopy(locals())
        uri = paystacklib.api_base + cls.object_type + '/enable'
        return cls(uri=uri, method='post', params=params)

    @classmethod
    def fetch(cls, id_or_subscription_code):
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(id_or_subscription_code))
        return cls(uri=uri, method='get').execute() 


