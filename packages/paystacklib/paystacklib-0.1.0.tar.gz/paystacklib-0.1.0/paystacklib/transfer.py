
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class Transfer(BaseApi):
    object_type = '/transfer'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)

    @classmethod
    def initiate(cls, amount, recipient, source='balance', currency=None,
            reason=None, reference=None): 
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type
        return cls(uri=uri, method='post', params=params).execute() 

    @classmethod
    def list(cls, perPage=None, page=None):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type 
        return cls(uri=uri, method='get', params=params).execute()

    @classmethod
    def fetch(cls, id_or_code):
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(id_or_code))
        return cls(uri=uri, method='get').execute() 

    @classmethod    
    def finalize(cls, transfer_code, otp):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/finalize_transfer' 
        return cls(uri=uri, method='post', params=params).execute()

    @classmethod
    def bulk(cls, transfers, currency, source='balance'):
        """
        transfers is in the form [{'amount': intval1, 'recipent': recipientcode1}, 
            {'amount': intval2, 'recipient': recipientcode2}, ...]
        """
        params = {'currency': currency, 'source': source, 'transfers': transfers}
        uri = paystacklib.api_base + cls.object_type + '/bulk'
        return cls(uri=uri, method='post', params=params).execute()

    @classmethod
    def check_balance(cls):
        uri = paystacklib.api_base + '/balance'
        return cls(uri=uri, method='get').execute()

    @classmethod
    def resend_otp(cls, transfer_code, reason):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/resend_otp'
        return cls(uri=uri, method='post', params=params).execute()

    @classmethod
    def disable_otp(cls):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/disable_otp'
        return cls(uri=uri, method='post', params=params).execute()

    @classmethod
    def disable_otp_finalize(cls, otp):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/disable_otp_finalize'
        return cls(uri=uri, method='post', params=params).execute()

    @classmethod
    def enable_otp(cls):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type + '/enable_otp'
        return cls(uri=uri, method='post', params=params).execute()
