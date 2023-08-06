
import paystacklib
from paystacklib.baseapi import BaseApi
from paystacklib.utils import clean_params
import copy

class BulkCharge(BaseApi):
    object_type = '/bulkcharge'
    def __init__(
            self, secret_key=None,
            uri=paystacklib.api_base + object_type, method=None, 
            headers=None, params=None):
        BaseApi.__init__(self, secret_key, uri, method, headers, params)


    @classmethod
    def initiate(cls, data):
        uri = paystacklib.api_base + object_type
        return cls(uri=uri, method='post', params=data).execute()

    @classmethod
    def list(cls, perPage=None, page=None):
        params = copy.deepcopy(locals())
        params = clean_params(params)
        uri = paystacklib.api_base + cls.object_type 
        return cls(uri=uri, method='get', params=params).execute()

    @classmethod
    def fetch_bulk_charge_batch(cls, id_or_code):
        uri = paystacklib.api_base + \
            '{0}/{1}'.format(cls.object_type, str(id_or_code))
        return cls(uri=uri, method='get').execute()


    @classmethod
    def fetch_charges_in_batch(cls, id_or_code, status=None, perPage=None,
            page=None):
        params = copy.deepcopy(locals())
        uri = paystacklib.api_base + \
            '{0}/{1}/charges'.format(cls.object_type, str(id_or_code))
        del params['id_or_code']
        params = clean_params(params)
        return cls(uri=uri, method='get', params=params).execute()

    @classmethod
    def pause(cls, batch_code):
        uri = paystacklib.api_base + \
            '{0}/pause/{1}'.format(cls.object_type, str(batch_code))
        return cls(uri=uri, method='get').execute()


    @classmethod
    def resume(cls, batch_code):
        uri = paystacklib.api_base + \
            '{0}/resume/{1}'.format(cls.object_type, str(batch_code))
        return cls(uri=uri, method='get').execute()

