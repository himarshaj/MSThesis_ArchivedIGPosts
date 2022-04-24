#!/usr/bin/env python3

import os
import datetime
from datetime import datetime, timedelta
import requests
import time
import random
import sys
import logging

'''
python3 curl_IG_collectDATA.py test_shortcode.txt summary.tsv block_info.csv
'''

logging.basicConfig(filename='instagram_data_collect.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


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
	shortcodes = file.readlines()
	#print(shortcodes)
	logging.info('Shortcode list obtained')
	file_out = sys.argv[2]#tsv file
	block_data = open(sys.argv[3],'w') 
	block_data.write("block_count,blocked_start,blocked_removed,diff.seconds\n")
	block_data.flush()
	block_count = 0
	with open(file_out,"w") as f:		
		for code in shortcodes:
			code = code.strip("\n")
			print(code)
			outfile = f"{code}.html"
			with open(outfile,"w") as g:
				url= f"https://www.instagram.com/p/{code}/"
				html, status_code, header_dic, blocked = issue_request(url)
				if blocked == False:
					#response recieved
					logging.info('Blocked = False, Response recieved')
					g.write(html)
				#redirected to login page
				elif blocked == True:
					#keep issuing request until unblocked
					#Entering the block period
					logging.info('Blocked = True, Entering the block period')
					block_count = block_count + 1
					html, status_code, header_dic, blocked = block_period(status_code,url,block_data,block_count)
					logging.info('Blocked = False, Block period ended')
					g.write(html)
				else:
					#logging
					pass
			f.write(f"{code}\t{status_code}\t{header_dic}\n")
			f.flush()
			#t =  + random.random()
			#time.sleep(t)
	block_data.close()
