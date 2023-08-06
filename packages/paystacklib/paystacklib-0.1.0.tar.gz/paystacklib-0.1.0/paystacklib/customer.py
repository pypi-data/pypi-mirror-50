
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class Customer(BaseApi):
    object_type = '/customer'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)

    @classmethod
    def create(
            cls, email, 
            first_name=None, last_name=None, phone=None, 
            metadata=None): 
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type
        return cls(uri=uri, method='post', params=params).execute() 


    @classmethod
    def list(
            cls, per_page=50, page=1): 
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type 
        return cls(uri=uri, method='get', params=params).execute()

    @classmethod
    def fetch(cls, email_or_id_or_customer_code):
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(email_or_id_or_customer_code))
        return cls(uri=uri, method='get').execute() 

    @classmethod    
    def update(
            cls, id_or_customer_code, first_name=None, 
            last_name=None, phone=None, metadata=None): 
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/id_or_customer_code'
        return cls(uri=uri, method='put', params=params).execute()


    @classmethod
    def set_risk_action(
            cls, customer, risk_action=None): 
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/set_risk_action'
        return cls(uri=uri, method='post', params=params).execute()

    @classmethod
    def deactivate_authorization(
            cls, authorization_code): 
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/deactivate_authorization'
        return cls(uri=uri, method='post', params=params).execute() 

