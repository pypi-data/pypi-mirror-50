import paystacklib
import os
from paystacklib.transaction import *
from paystacklib.customer import *

import unittest
paystacklib.secret_key = os.environ['PAYSTACK_SK']

class TransactionTests(unittest.TestCase):
    
    def test_transaction_initialize(self):
        tinit = Transaction.initialize(50000, "0@test.com")
        self.assertEqual(tinit['status'], True, 'Transaction initialization failed')

    def test_transaction_list_verify_fetch(self):
        tlist = Transaction.list()
        self.assertEqual(tlist['status'], True, 'Transaction list failed') 
        tref = tlist['data'][0]['reference']
        tid = tlist['data'][0]['id']
        tverify = Transaction.verify(tref)
        self.assertEqual(tverify['status'], True, 'Transaction verify failed')
        tfetch = Transaction.fetch(tid)
        self.assertEqual(tfetch['status'], True, 'Transaction fetch failed')
if __name__ == '__main__':
    unittest.main()

