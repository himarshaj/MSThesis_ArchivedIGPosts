#!/usr/bin/env python3

import io
import sys
import csv
import os
from datetime import datetime


#a_directory = "/home/marsh/Documents/Research/Thesis/MSThesis/IG_Archive/WARCs/response/run4_usernames"
a_directory = sys.argv[1]
#username = sys.argv[2]

def file_command(filepath):
	# #print(filepath)	
	# username = filepath.split("-")[2].split(".warc.")[0]
	# #print(username)
	# #Generate Revisit record
	# try:		
	# 	cmd = f"python3 warcio_write_urim_revisit.py {filepath} {username}"
	# 	#print(cmd)
	# except Exception as e:
	# 	#print(e)
	# 	pass
	
	#Indexing
	#print(filepath)
	cdx = (filepath.split("/")[3]).split(".")[0] + ".cdxj"
	cmd = f"cdxj-indexer {filepath} > CDXJ/{cdx}"

	os.system(cmd)

start = datetime.now()
for filename in os.listdir(a_directory):
	filepath = os.path.join(a_directory, filename)
	file_command(filepath)
	#break
end = datetime.now()
print("Start: " + str(start))
print("End: " + str(end))
print("Time taken: " + str(end - start))