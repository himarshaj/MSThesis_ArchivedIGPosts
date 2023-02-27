#!/usr/bin/env python3

import requests
import time
import sys

filename = sys.argv[1]
output = filename.split(.)[0] + ".csv" 

if __name__ == "__main__":
		filename1 = filename
		filename2 = "IGmedia_UIMs.csv"
		with open(filename1, "r") as f:
			URIMs = f.readlines()
		count = 1
		with open(filename2, "w") as g:
			g.write("urim,isRedirect,isCDN,FinalRedirectedURIM\n")
			for URIM in URIMs:
				URIM = URIM.strip("\n")
				#print(URIM)
				print(count)
				try:
					res = requests.head(URIM, allow_redirects=True)
					status_code = res.status_code
					history = res.history
					if history:
						isRedirect = True 
						final_redirect = history.pop()
						final_redirect_loc = final_redirect.headers['location']
						#status_code = final_redirect.status_code
						#print(final_redirect_loc)
						if "cdn".upper() in final_redirect_loc.upper():
							isCDN = True
							CDNURIM = final_redirect_loc
						if "save/_embed".upper() in final_redirect_loc.upper():
							isCDN = False
							CDNURIM = final_redirect_loc
							#print(final_redirect_loc)
					else:
						isRedirect = False
						isCDN = False
						CDNURIM = "-"
					#print(isRedirect,isCDN,status_code) 

				except Exception as e:
					# print(e)
					isRedirect = "error"
					isCDN = "error"
					CDNURIM = "error"
					print("skip")
					continue
				g.write(f"{URIM},{isRedirect},{isCDN},{CDNURIM}\n")
				g.flush()
				time.sleep(2)
				count = count + 1
				#break

