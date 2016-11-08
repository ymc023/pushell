#!/usr/bin/python2.7
import datetime

import pyotp
import qrcode


class TwoAuth:
    def __init__(self, secret=None):
        #if secret is None:
            #secret = pyotp.random_base32()
        self.secret = 'NFP7DMPDPEFK6I6S'
        self.totp = pyotp.TOTP(secret)

    def generate_token(self):
        print  self.totp.now()

    def valid(self, token):
        token = int(token)
        now = datetime.datetime.now()
        time30secsago = now + datetime.timedelta(seconds=-30)
#        try:
#            valid_now = self.totp.verify(token)
#            valid_past = self.totp.verify(token, for_time=time30secsago)
#            print valid_now
#            print valid_past 
#            return valid_now or valid_past
#        except:
#            print "error"
#            return False
#
    def qrcode(self, username):
        uri = self.totp.provisioning_uri(username)
        return qrcode.make(uri)


a=TwoAuth()
a.generate_token()
