#!/usr/bin/env python
# coding:utf8

import sys
import os

import pyotp
import qrcode


def genqrcode():
    code = pyotp.random_base32()
    str2qr(code)

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


if __name__ == '__main__': 
    genqrcode()
