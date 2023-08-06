import os



def get_header(secret_key=None):
    """
    Prepare header dict

    Args:
        secret_key: Paystack API secret key, retrieved from PAYSTACK_SK environment variable if not passed as argument
    Return:
        header dict
    """
    if not secret_key:
        secret_key = os.environ.get('PAYSTACK_SK')
    bearer = 'Bearer {0}'.format(secret_key)
    header = {'Authorization': bearer, 'Content-Type': 'application/json'}
    return header


def clean_params(params):
    params = {item:params[item] for item in params.keys() if params[item] is not None and item is not 'cls'}
    return params
