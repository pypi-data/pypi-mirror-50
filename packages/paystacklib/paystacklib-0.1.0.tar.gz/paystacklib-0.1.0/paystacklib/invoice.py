
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class Invoice(BaseApi):
    object_type = '/paymentrequest'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)

    @classmethod
    def create(
            cls, customer, amount, due_date, description=None,
            line_items=None, tax=None, currency=None, 
            metadata=None, send_notification=None, subaccount=None, 
            draft=None, has_invoice=None, invoice_number=None):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type 
        return cls(uri=uri, method='post', params=params).execute() 

    @classmethod    
    def verify(cls, invoice_code):
        uri = paystacklib.api_base + \
            '{0}/verify/{1}'.format(cls.object_type, invoice_code)
        return cls(uri=uri, method='get').execute()

    @classmethod
    def list(
            cls, customer=None, status=None, currency=None, 
            paid=None, include_archive=None): 
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type
        return cls(method='get', params=params).execute()

    @classmethod
    def view(cls, invoice_id_or_code):
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(invoice_id_or_code))
        return cls(uri=uri, method='get').execute() 

    @classmethod
    def notify(cls, id_or_code):
        uri = paystacklib.api_base + \
            '{0}/notify/{1}'.format(cls.object_type, str(id_or_code))
        return cls(uri=uri, method='post').execute()


    @classmethod
    def totals(cls):
        uri = paystacklib.api_base + cls.object_type + '/totals'
        return cls(uri=uri, method='get').execute()

    @classmethod
    def finalize(cls, id_or_code, send_notification=None):
        params = copy.deepcopy(locals())
        del params['id_or_code'] #not passed in body or as query param
        params = clean_params(params)
        uri = paystacklib.api_base + \
            '{0}/finalize/{1}'.format(cls.object_type, str(id_or_code))
        return cls(uri=uri, method='post').execute()

    @classmethod
    def update(
            cls, id_or_code, customer=None, amount=None, due_date=None,
            description=None, line_items=None, tax=None, currency=None,
            metadata=None, send_notification=None
            ):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(id_or_code))
        return cls(uri=uri, method='put', params=params).execute()

    @classmethod
    def archive(cls, id_or_code):
        uri = paystacklib.api_base + \
            'invoice/archive/{0}'.format(cls.object_type, str(id_or_code))
        return cls(uri=uri, method='post').execute()

