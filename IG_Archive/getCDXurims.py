#!/usr/bin/env python3

import io
import sys
import csv
import os



if __name__ == "__main__":
	with open("postURLs20.txt", "r") as f:
		URLs = f.readlines()

	with open("urims.csv", "w") as f:
		for ig_url in URLs:
			#print(shortcode,username)
			print(ig_url)
			ig_url = ig_url.strip("\n")
			url =  "http://web.archive.org/cdx/search/cdx?url=%s" % ig_url
			prefix = "https://web.archive.org/web/"
			awk = '{print "https://web.archive.org/web/" $2 "/" $3};'
			cmd = "curl -s %s | awk '%s' | head -58" % (url,awk)
			#cmd = "curl -s %s | awk '%s' " % (url,awk)
			#print(cmd)
			out = os.popen(cmd)
			urims = out.readlines()
			#print(urims)
			#l = len(urims)
			#print(ig_url,l)
			count = 0		
			for each in urims:		
				each = each.strip('\n')
				if "instagram.com:80" in each:
					#print(ig_url)
					pass
				else:
					#print(each)
					f.write(each + "\n")
					count = count + 1
				if count == 50:
					break
		