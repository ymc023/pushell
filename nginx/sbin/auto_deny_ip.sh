#!/usr/bin/sh  

#Author: ymc023
#Mail:  ymc023@163.com 
#Platform: centos7.1
#Date:Tue 30 Aug 2016 03:29:23 PM CST

max=60
deny_ip_dir=/usr/local/nginx/conf/vhost/deny_ip.conf
logdir=/usr/local/nginx/logs/www.hlxy.log/www.hlxy.com_access.log
deny_ip_log=/usr/local/nginx/logs/deny_ip_log.log
start_time=`date -d"$last_minutes minutes ago" +"%H:%M:%S"`
stop_time=`date +"%H:%M:%S"`
last_log=/usr/local/nginx/logs/last_minutes_nginx.log
ip="222.177.27.253"


function exec_last_minutes_nginx_log(){

 tac $logdir |awk -v st="$start_time" -v op="$stop_time" '
 {
  t=substr($4,14,21)
  if (t>=st && t<=op)
     {print $0 >>"/usr/local/nginx/logs/last_minutes_nginx.log";}

 }
'
if [ $? -eq 0 ];then
	return 0;
else
	return 1;
fi

}

function deny_ip(){

tail  $last_log | awk '{print $1}'|sort|uniq -c|sort -n|while read line
do
  l=(`echo $line`)
  if [ $l -ge $max ]; then
     ip1="${l[1]}"
     if [ $ip1 == $ip ]; then
         break
     else
        echo "deny ${l[1]};" >>$deny_ip_dir
     fi
  fi
done
}

function test_nginx_config(){
 /usr/local/nginx/sbin/nginx -t >/dev/null 2>&1
 if [ $? -eq 0 ]; then
    /usr/local/nginx/sbin/nginx -s reload 
    if [ $? -eq 0 ]; then
    echo " `date`   now reload nginx ok!" >>$deny_ip_log &&  >/dev/null 2>&1
    fi
 fi

}

exec_last_minutes_nginx_log
 if [ -s $last_log ]; then
        echo "last_log not null"
  	deny_ip
 else
        echo "last_log is null"
 	break;
 fi
 if [ $? -eq 0 ] && [ -s $deny_ip_dir ];then
 	test_nginx_config
 fi
cat /dev/null >$last_log
