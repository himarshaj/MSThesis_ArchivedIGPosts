#!/usr/bin/env python3

from warcio.archiveiterator import ArchiveIterator
import sys

file = sys.argv[1]

with open(file, 'rb') as fh:	
    for record in ArchiveIterator(fh):
    	#headers
    	#print(record.http_headers)
    	#record headers
    	print(record.rec_headers)
    	#payload
    	print(record.content_stream().read())