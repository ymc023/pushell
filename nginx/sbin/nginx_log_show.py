#!/usr/bin/env python
# coding=utf-8

#Author: ymc023
#Mail: ymc023@163.com 
#Platform: centos7.1
#Date:Tue 30 Aug 2016 10:31:27 AM CST

import sys 
import time 
import os

#用来打印格式生成 
class displayFormat(object): 
	def format_size(self,size): 
		'''''格式化单位''' 
		KB = 1024		    #KB 
		MB = 1048576		#MB 
		GB = 1073741824	    #GB 
		TB = 1099511627776  #TB 
		if size >= TB : 
			size = str(size / TB) + 'T' 
		elif size < KB : 
			size = str(size) + 'B' 
		elif size >= GB and size < TB: 
			size = str(size / GB) + 'G' 
		elif size >= MB and size < GB : 
			size = str(size / MB) + 'M' 
		else : 
			size = str(size / KB) + 'K' 
		return size 
 
	#定义字符串格式化 
	formatstring = '%-15s %-10s %-12s %8s %10s %10s %10s %10s %10s %10s %10s' 
 
	def transverse_line(self) : 
		'''''输出横线''' 
		print self.formatstring % ('-'*15,'-'*10,'-'*12,'-'*12,'-'*10,'-'*10,'-'*10,'-'*10,'-'*10,'-'*10,'-'*10) 
 
	def head(self): 
		'''''输出头部信息''' 
		print self.formatstring %('IP','Traffic','Times','Times%','200','302','304','403','404','500','503') 
 
	def error_print(self) : 
		'''''输出错误信息''' 
		print 
		print 'Usage : ' + sys.argv[0] + ' NginxLogFilePath [Number]' 
		print 
		sys.exit(1) 
 
	def execut_time(self): 
		'''''输出脚本执行的时间''' 
		print 
		print "Script Execution Time: %.3f "  % time.clock() 
		print 
 
#该类是用来生成主机信息的字典 
class hostInfo(object): 
	host_info = ['200','404','500','302','304','503','403','times','size'] 
 
	def __init__(self,host): 
		self.host = host = {}.fromkeys(self.host_info,0) 
 
	def increment(self,status_times_size,is_size): 
		'''''该方法是用来给host_info中的各个值加1''' 
		if status_times_size == 'times': 
			self.host['times'] += 1 
		elif is_size: 
			self.host['size'] = self.host['size'] + status_times_size 
		else: 
			self.host[status_times_size] += 1 
 
	def get_value(self,value): 
		'''''该方法是取到各个主机信息中对应的值''' 
		return self.host[value] 
 
#该类是用来分析文件 
class fileAnalysis(object): 
	def __init__(self): 
		'''''初始化一个空字典''' 
		self.report_dict = {} 
		self.total_request_times,self.total_traffic,self.total_200, \
		self.total_404,self.total_500,self.total_403,self.total_302, \
		self.total_304,self.total_503 = 0,0,0,0,0,0,0,0,0 
 
	def split_eachline_todict(self,line): 
		'''''分割文件中的每一行，并返回一个字典''' 
		split_line = line.split() 
		split_dict = {'remote_host':split_line[0],'status':split_line[8], \
					  'bytes_sent':split_line[9],} 
		return  split_dict 
 
	def generate_log_report(self,logfile): 
		'''''读取文件，分析split_eachline_todict方法生成的字典''' 
		for line in logfile: 
			try: 
				line_dict = self.split_eachline_todict(line) 
				host = line_dict['remote_host'] 
				status = line_dict['status'] 
			except ValueError : 
				continue 
			except IndexError : 
				continue 
 
			if host not in self.report_dict : 
				host_info_obj = hostInfo(host) 
				self.report_dict[host] = host_info_obj 
			else : 
				host_info_obj = self.report_dict[host] 
 
			host_info_obj.increment('times',False)  
			if status in host_info_obj.host_info : 
				host_info_obj.increment(status,False)  
			try: 
				bytes_sent = int(line_dict['bytes_sent']) 
			except ValueError: 
				bytes_sent = 0 
			host_info_obj.increment(bytes_sent,True)  
		return self.report_dict 
 
	def return_sorted_list(self,true_dict): 
		'''''计算各个状态次数、流量总量，请求的总次数，并且计算各个状态的总量 并生成一个正真的字典，方便排序''' 
		for host_key in true_dict : 
			host_value = true_dict[host_key] 
			times = host_value.get_value('times')						
			self.total_request_times = self.total_request_times + times  
			size = host_value.get_value('size')						
			self.total_traffic = self.total_traffic + size   
 
			o200 = host_value.get_value('200') 
			o404 = host_value.get_value('404') 
			o500 = host_value.get_value('500') 
			o403 = host_value.get_value('403') 
			o302 = host_value.get_value('302') 
			o304 = host_value.get_value('304') 
			o503 = host_value.get_value('503') 
 
			true_dict[host_key] = {'200':o200,'404':o404,'500':o500, \
								   '403':o403,'302':o302,'304':o304, \
								   '503':o503,'times':times,'size':size} 
 
			self.total_200 = self.total_200 + o200 
			self.total_404 = self.total_404 + o404 
			self.total_500 = self.total_500 + o500 
			self.total_302 = self.total_302 + o302 
			self.total_304 = self.total_304 + o304 
			self.total_503 = self.total_503 + o503 
 
		sorted_list = sorted(true_dict.items(),key=lambda t:(t[1]['times'],\
															 t[1]['size']),reverse=True) 
 
		return sorted_list 
 
class Main(object): 
	def main(self) : 
		'''''主调函数''' 
		display_format = displayFormat() 
		arg_length = len(sys.argv) 
		if arg_length == 1 : 
			display_format.error_print() 
		elif arg_length == 2 or arg_length == 3: 
			infile_name = sys.argv[1] 
			try : 
				infile = open(infile_name,'r') 
				if arg_length == 3 : 
					lines = int(sys.argv[2]) 
				else : 
					lines = 0 
			except IOError,e : 
				print 
				print e 
				display_format.error_print() 
			except ValueError : 
				print 
				print "Please Enter A Volid Number !" 
				display_format.error_print() 
		else : 
			display_format.error_print() 
 
		fileAnalysis_obj = fileAnalysis() 
		not_true_dict = fileAnalysis_obj.generate_log_report(infile) 
		log_report = fileAnalysis_obj.return_sorted_list(not_true_dict) 
		total_ip = len(log_report) 
		if lines : 
			log_report = log_report[0:lines] 
		infile.close() 
 
		print 
		total_traffic = display_format.format_size(fileAnalysis_obj.total_traffic) 
		total_request_times = fileAnalysis_obj.total_request_times 
		print 'Total IP: %s   Total Traffic: %s   Total Request Times: %d' \
			  % (total_ip,total_traffic,total_request_times) 
		print 
		display_format.head() 
		display_format.transverse_line() 
 
		for host in log_report : 
			times = host[1]['times'] 
			times_percent = (float(times) / float(fileAnalysis_obj.total_request_times)) * 100 
			print display_format.formatstring % (host[0],\
												 display_format.format_size(host[1]['size']),\
												 times,str(times_percent)[0:5],\
												 host[1]['200'],host[1]['302'],\
												 host[1]['304'],host[1]['403'],\
												 host[1]['404'],host[1]['500'],host[1]['503']) 
												  
		if (not lines) or total_ip == lines : 
			display_format.transverse_line() 
			print display_format.formatstring % (total_ip,total_traffic, \
												 total_request_times,'100%',\
												 fileAnalysis_obj.total_200,\
												 fileAnalysis_obj.total_302,\
												 fileAnalysis_obj.total_304, \
												 fileAnalysis_obj.total_403,\
												 fileAnalysis_obj.total_404, \
												 fileAnalysis_obj.total_500,\
												 fileAnalysis_obj.total_503) 
 
		display_format.execut_time() 
 
if __name__ == '__main__': 
	main_obj = Main() 
	main_obj.main()
