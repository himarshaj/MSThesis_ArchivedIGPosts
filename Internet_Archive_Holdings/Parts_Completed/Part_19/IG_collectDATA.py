#!/usr/bin/env python3

'''
Code Usage:
python3 IG_collectDATA.py shortcodeaa shortcodeaa_out.tsv shortcodeaa_blockdata.csv

This code will go through each shortcode in the input file and download the HTML. 
Instagram will temporarily redirect the requests to its login page after a couple of 
requests and this code will wait the penalty period and continue collecting the data.

shortcodeaa - A text file containing the shortcodes of Instagram posts to be downloaded (Input)
shortcodeaa_out.tsv - A summary file containing the response status code & headers (Output)
shortcodeaa_blockdata.csv - A CSV file containg information about the penalty period (Output)
shortcodeaa_requests.log - log file (Output) 
'''

import os
import datetime
from datetime import datetime, timedelta
import requests
import time
import random
import sys
import logging
import re

logging.basicConfig(filename=f'{sys.argv[1]}_requests.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def issue_request(url):
	out = requests.get(url, allow_redirects=False)
	status_code = out.status_code
	html = out.text
	header_dic = out.headers
	logging.info('Request Issued')
	if status_code == 200:
		blocked = False
	elif status_code == 302:
		location = out.headers['Location']
		'''out.headers['Location']
		'https://www.instagram.com/accounts/login/?next=/p/CY4sYM-hYI3/'
		'''
		if "https://www.instagram.com/accounts/login/" in location:
			logging.info('Blocked')
			blocked = True
		else:
			blocked = "NA"
	else:
		blocked = "NA"
	return html, status_code, header_dic, blocked

def block_period(status_code,url,block_data,block_count):
	blocked_start = datetime.now()
	while status_code == 302:
		#checking every 30 mins
		time.sleep(1800)
		html, status_code, header_dic, blocked = issue_request(url)
	#blocked = False
	blocked_removed = datetime.now()
	diff = blocked_removed - blocked_start
	block_data.write(f"{block_count},{blocked_start},{blocked_removed},{diff.seconds}\n")
	block_data.flush()
	logging.info(f'Block ID: {block_count}, Block period: {diff.seconds} seconds')
	return html, status_code, header_dic, blocked

if __name__ == "__main__":
	logging.info('Started')
	file = open(sys.argv[1],'r')  #text file with shortcode
	try:
		file2 = open(f'{sys.argv[1]}_done','r')
		donecodes = set(line.strip() for line in file2)
		file2.close()
	except:
		donecodes = set()
	shortcodes = file.readlines()
	#print(shortcodes)
	logging.info('Shortcode list obtained')
	file_out = f'{sys.argv[1]}_out.tsv' #sys.argv[2]#tsv file
	block_data = open(f'{sys.argv[1]}_blockdata.csv','w')   #sys.argv[3],'w') #	 file
	block_data.write("block_count,blocked_start,blocked_removed,diff.seconds\n")
	block_data.flush()
	block_count = 0
	with open(file_out,"a") as f:	
		print("Start of data collection")	
		count = 1
		count = count + len(donecodes)
		print(f"\nCount, Shortcode")
		for code in shortcodes:
			code = code.strip("\n")
			if code in donecodes:
				continue
			print(f"{count}, {code}")
			outfile = f"HTML_out/{code}.html"
			with open(outfile,"w",encoding='utf8', errors='ignore') as g:
				url= f"https://www.instagram.com/p/{code}/"
				html, status_code, header_dic, blocked = issue_request(url)
				if blocked == False:
					#response recieved
					logging.info('Blocked = False, Response recieved')
					g.write(html)
					file3 = open(f'{sys.argv[1]}_done','a')
					file3.write(f"{code}\n")
					file3.close()
				#redirected to login page
				elif blocked == True:
					#keep issuing request until unblocked
					#Entering the block period
					logging.info('Blocked = True, Entering the block period')
					block_count = block_count + 1
					print("Blocked")
					sys.exit()
					html, status_code, header_dic, blocked = block_period(status_code,url,block_data,block_count)
					logging.info('Blocked = False, Block period ended')
					g.write(html)
				else:
					#not 200 status code					
					file3 = open(f'{sys.argv[1]}_done','a')
					file3.write(f"{code}\n")
					file3.close()
					#logging
					pass
			f.write(f"{code}\t{status_code}\t{header_dic}\n")
			f.flush()
			count = count + 1
			t = 10 + random.random()
			time.sleep(t)		
		print("\nEnd of data collection")	
	block_data.close()
