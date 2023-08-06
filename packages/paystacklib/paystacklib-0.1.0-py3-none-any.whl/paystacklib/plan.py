
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class Plan(BaseApi):
    object_type = '/plan'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)

    @classmethod
    def create(
            cls, name, amount, interval, description=None, send_invoices=None,
            send_sms=None, currency=None, invoice_limit=None):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type
        return cls(uri=uri, method='post', params=params).execute() 


    @classmethod
    def list(
            cls, per_page=50, page=1, interval=None, amount=None): 
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type 
        return cls(uri=uri, method='get', params=params).execute()

    @classmethod
    def fetch(cls, id_or_plan_code):
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(id_or_plan_code))
        return cls(uri=uri, method='get').execute() 

    @classmethod    
    def update(
            cls, id_or_plan_code, name=None, 
            amount=None, description=None, send_invoices=None,
            send_sms=None, currency=None, invoice_limit=None): 
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(id_or_plan_code)) 
        return cls(uri=uri, method='put', params=params).execute()

