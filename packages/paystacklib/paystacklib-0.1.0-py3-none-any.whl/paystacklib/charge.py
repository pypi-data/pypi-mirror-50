
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class Charge(BaseApi):
    object_type = '/charge'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)

    @classmethod
    def charge(
            cls, amount, email, 
            bank_code=None, bank_account_number=None, 
            authorization_code=None, pin=None, metadata=None, reference=None, 
            ussd_type=None, mobile_money=None, device_id=None):
        bank_object = None 
        ussd_object = None
        if bank_code and bank_account_number:
            bank_object = {}
            bank_object['code'] = str(bank_code)
            bank_object['account_number'] = str(bank_account_number)
        if ussd_type:
            ussd_object = {}
            ussd_object['type'] = ussd_type 
        params = {'amount': amount, 'email': email, 'bank': bank_object, 
            'authorization_code': authorization_code, 'pin': pin,
            'metadata': metadata, 'reference': reference, 'ussd': ussd_object,
            'mobile_money': mobile_money, 'device_id': device_id}
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type 
        return cls(uri=uri, method='post', params=params).execute() 

    @classmethod    
    def submit_pin(cls, pin, reference):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/submit_pin' 
        return cls(uri=uri, method='post', params=params).execute()

    @classmethod    
    def submit_otp(cls, otp, reference):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/submit_otp'
        return cls(uri=uri, method='post', params=params).execute()
    
    @classmethod
    def submit_phone(cls, phone, reference):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/submit_phone'
        return cls(uri=uri, method='post', params=params).execute()

    @classmethod
    def submit_birthday(cls, birthday, reference):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/submit_birthday'
        return cls(uri=uri, method='post', params=params).execute()


    @classmethod
    def check_pending_charge(cls, reference):
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(reference))
        return cls(uri=uri, method='get').execute() 


