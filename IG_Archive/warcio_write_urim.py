#!/usr/bin/env python3
                 
#import otmt
import glob
from warcio.warcwriter import WARCWriter
from warcio.statusandheaders import StatusAndHeaders
from hashlib import md5
from datetime import datetime
import traceback
import requests
import csv

def create_warc(urim, raw_urim, output_directory, username):

    m = md5()
    m.update(urim.encode('utf8'))
    urlhash = m.hexdigest()

    resp = requests.get(urim, stream=True)
    resp.raise_for_status()

    headers_list = resp.raw.headers.items()

    raw_response = requests.get(raw_urim, stream=True)

    warc_target_uri = None

    # we have to implement this construct in case the archive combines original with other relations
    for link in resp.links:

        if 'original' in link:
            warc_target_uri = resp.links[link]['url']

    if warc_target_uri is None:
        module_logger.warning("could not find this memento's original resource, skipping {}".format(urim))
        return

    try:
        mdt = resp.headers['Memento-Datetime']

    except KeyError:
        print("could not find this memento's memento-datetime, skipping {}".format(urim))
        return

    http_headers = StatusAndHeaders('200 OK',
        headers_list, protocol='HTTP/1.0')

    # module_logger.debug("mdt formatted by strptime and converted by strftime: {}".format(
    #     datetime.strptime(
    #         mdt, "%a, %d %b %Y %H:%M:%S GMT"
    #     ).strftime('%Y-%m-%dT%H:%M:%SZ')
    # ))

    warc_headers_dict = {}
    # warc_target_uri = "https://twitter.com/realDonaldTrump/status/1338871862315667456"
    # warc_headers_dict['WARC-Refers-To'] = "<urn:uuid:1c88a09f-8bd4-4cb9-82a0-69cc92078204>"
    # warc_headers_dict['WARC-Profile'] = "http://netpreserve.org/warc/1.1/revisit/identical-payload-digest"
    # warc_headers_dict['WARC-Refers-To-Target-URI'] = "http://instagram.com/p/D/"
    # warc_headers_dict['WARC-Refers-To-Date'] = "2019-10-25T02:36:18Z"
    warc_headers_dict['WARC-Date'] = datetime.strptime(
        mdt, "%a, %d %b %Y %H:%M:%S GMT"
    ).strftime('%Y-%m-%dT%H:%M:%SZ')

    with open("{}/{}-{}-{}.warc.gz".format(output_directory, urlhash, datetime.now().strftime('%Y%m%d%H%M%S'),username), 'wb') as output:
        writer = WARCWriter(output, gzip=True)

       
        record = writer.create_warc_record(warc_target_uri, 'response',
                                        payload=resp.raw,
                                        http_headers=http_headers,
                                        warc_headers_dict=warc_headers_dict)

        writer.write_record(record)


if __name__ == "__main__":
    start = datetime.now()
    with open("urims.csv") as f:
        urims = f.readlines()


    urim_list = []

    for item in urims:
        urim = item.strip("\n")
        parts = urim.split("/web/")        
        urir = parts[1].split("/",1)[1]
        raw_urim = parts[0] + '/web/' + parts[1].split("/",1)[0] + 'mp_/' + urir
        with open("post_user_mapping.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == urir:
                    username = row[1]
                else:
                    pass
        #print(username)
        tuple = (urim,raw_urim,username)
        urim_list.append(tuple)
    #print(urim_list)
    #to get username - temporory fix
    #username = "sda"
    output_directory = "/home/marsh/Documents/Research/Thesis/MSThesis/IG_Archive/WARCs/response"
    count = 0
    for each in urim_list:
        urim = each[0]
        raw_urim = each[1]
        username = each[2]
        try:
            create_warc(urim, raw_urim, output_directory,username)
        except Exception as e:
            #print(e)
            print(urim)
        count = count + 1
        print(count)
        #break
    end = datetime.now()
    print("Start: " + str(start))
    print("End: " + str(end))
    print("Time taken: " + str(end - start))
