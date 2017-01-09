#!/usr/bin/env python
# coding=utf8

#Author:ymc023
#Mail:ymc023@163.com 
#Platform:Centos7
#Date:Tue 01 Jan 2017 03:10:40 PM CST

'''
Usage: 
    ./pushelld.py [status] [stop] [start] [restart]

Options:
    status  "查看服务状态" 
    stop    "停止服务"
    start   "启动服务"
    restart "重新启动服务"

Examples:

    ./pushelld.py status 

'''

import sys
import time
import os
import shlex

from docopt import docopt


PUSHELLDIR=os.path.abspath(os.curdir)
RUN_SERVER='%s/run_server.py'%PUSHELLDIR

def bash(cmd):
    return shlex.os.system(cmd)
def color_print(msg,color='red'):
    color_dict = {'yellow':'\033[1;33m%s\033[0m',
                 'green':'\033[1;32m%s\033[0m',
                  'red':'\033[1;31m%s\033[0m'
            }
    msg = color_dict.get(color,'red') %msg
    return msg
def pushelld():
    arg = docopt(__doc__)
    if arg['status']:
        if str(bash("ps aux | grep 'run_server' | grep -v 'grep'")) in '0':
            print (color_print('pushell is running ......','green'))
        else:
            print (color_print('pushell is not running ......','red'))
    if arg['stop']:
        if str(bash("ps aux | grep -E 'run_server.py' | grep -v grep | awk '{print $2}' | xargs kill\
 -9 &>/dev/null")) in '0':
            print(color_print('pushell is stop.','red'))
        else:
            print(color_print('pushell is not stop.','yellow'))
    if arg['start']:
        print(RUN_SERVER)
        if str(bash("python %s &" %RUN_SERVER)) in '0':
            print(color_print('pushell start is ok.','green'))
        else:
            print(color_print('pushell must be running as root.','red'))
    if arg['restart']:
        if str(bash("ps aux | grep -E 'run_server.py' | grep -v grep | awk '{print $2}' | xargs kill\
 -9 &> /dev/null")) in '0' and str(bash("python %s &" %RUN_SERVER)) in '0':
            print(color_print('pushell restart ok.','green'))
        else:
            print(color_print('pushell restart error.','red'))

if __name__ == '__main__':
    pushelld()
