#!/usr/bin/bash

#Author:ymc023
#Mail:ymc023@163.com 
#Platform:centos7.1
#Date:Mon 05 Sep 2016 02:18:29 PM CST


nginx_pid="/usr/local/nginx/logs/nginx.pid"

function cut_b2_hlxy {
nginx_log_dir="/usr/local/nginx/logs/b2.hlxy.log/"
nginx_log_name="b2.hlxy.com_access.log"
nginx_pid="/usr/local/nginx/logs/nginx.pid"
new_nginx_log_name=`date +'%Y%m%d'`_$nginx_log_name
mv ${nginx_log_dir}${nginx_log_name} ${nginx_log_dir}${new_nginx_log_name}
if [ $? -eq 0 ];then
	return 0
else
	return 1
fi
}

function cut_www_hlxy {
nginx_log_dir="/usr/local/nginx/logs/www.hlxy.log/"
nginx_log_name="www.hlxy.com_access.log"
nginx_pid="/usr/local/nginx/logs/nginx.pid"
new_nginx_log_name=`date +'%Y%m%d'`_$nginx_log_name
mv ${nginx_log_dir}${nginx_log_name} ${nginx_log_dir}${new_nginx_log_name}
echo "cut bank"
if [ $? -eq 0 ]; then
	return 0
else
	return 1
fi
}
function cut_bank_hlxy {

nginx_log_dir="/usr/local/nginx/logs/bank.hlxy.log/"
nginx_log_name="bank.hlxy.com_access.log"
nginx_pid="/usr/local/nginx/logs/nginx.pid"
new_nginx_log_name=`date +'%Y%m%d'`_$nginx_log_name
mv ${nginx_log_dir}${nginx_log_name} ${nginx_log_dir}${new_nginx_log_name}
echo "cut_bank"
if [ $? -eq 0 ];then
	return 0
else 
	return 1
fi
}

function cut_m_hlxy {
nginx_log_dir="/usr/local/nginx/logs/m.hlxy.log/"
nginx_log_name="m.hlxy.com_access.log"
nginx_pid="/usr/local/nginx/logs/nginx.pid"
new_nginx_log_name=`date +'%Y%m%d'`_$nginx_log_name
mv ${nginx_log_dir}${nginx_log_name} ${nginx_log_dir}${new_nginx_log_name}
if [ $? -eq 0 ];then 
	return 0
else
	return 1
fi
}

function cut_res() {
cut_b2_hlxy
b2_res=$?
cut_www_hlxy
www_res=$?
cut_bank_hlxy
bank_res=$?
cut_m_hlxy
m_res=$?

if [ $b2_res -eq 0 ]&& [ $www_res -eq 0 ]&& [ $bank_res -eq 0 ]&& [ $m_res -eq 0 ];then
	return 0
else
	return 1
fi

}

cut_res
res=$?
if [ $res -eq 0 ];then
	kill -USR1 `cat $nginx_pid` 
        if [ $? -eq 0 ];then
        	echo "`date`  rebuild nginx log ok!" >>/usr/local/nginx/logs/cut_nginx_log.log
        fi
fi

