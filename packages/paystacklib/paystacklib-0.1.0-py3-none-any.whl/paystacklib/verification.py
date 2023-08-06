
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class Verification(BaseApi):
    object_type = '/verification'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)

    @classmethod
    def resolve_bvn(cls, bvn):
        uri = paystacklib.api_base + '/bank/resolve_bvn/{0}'.format(str(bvn)) 
        return cls(uri=uri, method='get').execute() 
    
    #@classmethod
    #def match_bvn(cls, account_numer, bank_code, bvn,
    #        first_name=None, middle_name=None, last_name=None):
    #    params = copy.deepcopy(locals())
    #    params = clean_params(params)
    #    uri = paystacklib.api_base + '/bvn/match'
    #    return cls(uri=uri, method='post', params=params).execute()

    @classmethod
    def resolve_account_number(cls, account_number, bank_code):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + '/bank/resolve'
        return cls(uri=uri, method='get', params=params).execute()

    @classmethod
    def resolve_card_bin(cls, card_bin):
        uri = paystacklib.api_base + '/decision/bin/{0}'.format(str(card_bin))
        return cls(uri=uri, method='get').execute()

    @classmethod
    def resolve_phone_number(cls, verification_type, phone, callback_url):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + '/verifications'
        return cls(uri=uri, method='post', params=params).execute()

