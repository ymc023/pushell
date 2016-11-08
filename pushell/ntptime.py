#!/usr/bin/env python
# coding:utf8

import sys
import time
from time import  ctime
import socket
import struct

import ntplib


NTP_SERVER = '1.cn.pool.ntp.org'
TIME1970 = 2208988800L


def print_time():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('1.cn.pool.ntp.org')
    #  print ctime(response.tx_time)
    # print response.tx_time


def sntp_client():
    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    data = '\x1b' +47 * '\0'
    client.sendto(data, (NTP_SERVER, 123))
    data,address = client.recvfrom(1024)
    if data:
        print 'from:',address
    t = struct.unpack('!12I',data) [10]
    t -= TIME1970
    print '\tTime=%s' %time.ctime(t)



if __name__ == '__main__': 
    sntp_client()
