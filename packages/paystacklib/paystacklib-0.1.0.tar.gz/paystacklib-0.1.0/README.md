# paystack-lib-python
This library provides a Python implementation of the Paystack API.

## Installation
```
pip3 install --upgrade paystacklib
```

## Requirements
Python 3.5+

## Usage
The Paystack secret key should be defined in the Environment as `PAYSTACK_SK` or assigned to `paystacklib.secret_key`

```
>>> import paystacklib
>>> paystacklib.secret_key = 'sk_your_paystack_secret_key' 
>>> transaction = paystacklib.Transaction.initialize(500000, 'customer@customer.com')
>>> transaction
{'status': True, 'message': 'Authorization URL created', 
    'data': {'authorization_url': 'https://checkout.paystack.com/6rklpsq157c8bef', 
        'access_code': '6rklpsq157c8bef', 'reference': 'i1wdh5b2r3'}}
>>> transaction.status
True
>>> transaction.message
'Authorization URL created'
>>> transaction.data.authorization_url
'https://checkout.paystack.com/6rklpsq157c8bef'
>>> transaction.data.access_code
'6rklpsq157c8bef'
>>> transaction.data.reference
'i1wdh5b2r3'
>>> transaction['status'] #you can also access values this way
True
>>> transaction.whatever  #accessing non-existent element will return a 'False' value
{}
```

