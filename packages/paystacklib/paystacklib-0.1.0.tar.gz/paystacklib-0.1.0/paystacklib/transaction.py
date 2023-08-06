
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class Transaction(BaseApi):
    object_type = '/transaction'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)

    @classmethod
    def initialize(
            cls, amount, email, 
            callback_url=None, reference=None, plan=None, 
            invoice_limit=None, metadata=None, subaccount=None, 
            transaction_charge=None, bearer=None, channels=None):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/initialize'
        return cls(uri=uri, method='post', params=params).execute() 

    @classmethod    
    def verify(cls, reference):
        uri = paystacklib.api_base + \
            '{0}/verify/{1}'.format(cls.object_type, reference)
        return cls(uri=uri, method = 'get').execute()

    @classmethod
    def list(
            cls, per_page=50, page=1, 
            customer=None, status=None, fr=None, 
            to=None, amount=None):
        params = copy.deepcopy(locals())
        params['from'] = params['fr']
        del params['fr']
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type
        return cls(method='get', params=params).execute()

    @classmethod
    def fetch(cls, transaction_id):
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(transaction_id))
        return cls(uri=uri, method='get').execute() 

    @classmethod    
    def charge(
            cls, authorization_code, amount, 
            email, reference=None, plan=None, 
            currency=None, metadata=None, subaccount=None, 
            transaction_charge=None, bearer=None, invoice_limit=None, 
            queue=None):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/charge_authorization'
        return cls(uri=uri, method='post', params=params).execute()

    @classmethod
    def check_authorization(cls, authorization_code, amount, email,
            currency=None):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/check_authorization'
        return cls(uri=uri, method='post', params=params).execute() 

    @classmethod
    def timeline(cls, transaction_id):
        uri = paystacklib.api_base + \
            '{0}/timeline/{1}'.format(cls.object_type, str(transaction_id))
        return cls(uri=uri, method='get').execute()

    @classmethod
    def totals(cls, fr=None, to=None):
        params = copy.deepcopy(locals())
        params['from'] = params['fr']
        del params['fr']
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/totals'
        return cls(uri=uri, method='get', params=params).execute()

    @classmethod
    def export(
            cls, fr=None, to=None, 
            settled=None, payment_page=None, customer=None, 
            currency=None, settlement=None, amount=None, status=None):
        params = copy.deepcopy(locals())
        params['from'] = params['fr']
        del params['fr']
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/export'
        return cls(uri=uri, method='get', params=params).execute()

    @classmethod
    def request_reauthorization(
            cls, authorization_code, amount, 
            email, reference=None, metadata=None):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + \
            '/request_reauthorization'
        return cls(uri=uri, method='post', params=params).execute()

