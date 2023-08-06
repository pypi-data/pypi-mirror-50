
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class SubAccount(BaseApi):
    object_type = '/subaccount'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)

    @classmethod
    def create(
            cls, business_name, settlement_bank, account_number, 
            percentage_charge, primary_contact_email=None, 
            primary_contact_name=None, primary_contact_phone=None, 
            metadata=None, settlement_schedule=None): 
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
    def fetch(cls, id_or_slug):
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(id_or_slug))
        return cls(uri=uri, method='get').execute() 

    @classmethod    
    def update(
            cls, id_or_slug, business_name=None, settlement_bank=None, 
            account_number=None, percentage_charge=None,
            primary_contact_email=None, description=None, 
            primary_contact_name=None, primary_contact_phone=None,
            metadata=None, settlement_schedule=None): 
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(id_or_slug)) 
        return cls(uri=uri, method='put', params=params).execute()

