#!/usr/bin/python2.7 
# coding:utf8

import datetime
import  os
import sys

import pyotp
import qrcode

class TwoAuth():
    def __init__ (self,secret='NFP7DMPDPEFK6I6S'):
        self.secret = 'NFP7DMPDPEFK6I6S'
        self.totp = pyotp.TOTP(secret)
    def gen_token(self):
        print self.totp.now()
    def verify(self,token):
        token = int(token)
        now = datetime.datetime.now()
        sec30ago = now + datetime.timedelta(seconds=-30)
        try:
            if self.totp.verify(token) or self.totp.verify(sec30ago):
                return True
            else:
                return False
        except:
            return False

    def str2qr(str):
        qr = qrcode.QRCode()
        qr.boder = 1 
        qr.add_data(str)
        mat = qr.get_matrix()
        printQR(mat)
    def printQR(mat):
        for i in mat:
            BLACK = '\033[40m  \033[0m'
            WHITE = '\033[47m  \033[0m'
            print ''.join([BLACK if j else WHITE for j in i])



