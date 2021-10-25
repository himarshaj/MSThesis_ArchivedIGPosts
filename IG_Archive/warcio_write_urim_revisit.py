#!/usr/bin/env python3
                 
#import otmt
import glob
from warcio.warcwriter import WARCWriter
from warcio.statusandheaders import StatusAndHeaders
from warcio.archiveiterator import ArchiveIterator
from hashlib import md5
from datetime import datetime
import traceback
import requests
import sys

warc = sys.argv[1]
#out_folder = sys.argv[1]
#urim = sys.argv[2]
#raw_urim = sys.argv[3]
username = sys.argv[2] #username
#out_folder = sys.argv[3] #username
output_directory = f"/home/marsh/Documents/Research/Thesis/MSThesis/IG_Archive/WARCs/revisit/"


def read_warc():
    with open(warc, 'rb') as fh:    
        for record in ArchiveIterator(fh):
            record_id = record.rec_headers.get_header('WARC-Record-ID')
            target_uri = record.rec_headers.get_header('WARC-Target-URI')
            date = record.rec_headers.get_header('WARC-Date')
            http_headers = record.http_headers
    return record_id, target_uri, date, http_headers


def create_warc_revisit():

    # m = md5()
    # m.update(urim.encode('utf8'))
    # urlhash = m.hexdigest()

    # resp = requests.get(urim, stream=True)
    # resp.raise_for_status()

    # headers_list = resp.raw.headers.items()

    # raw_response = requests.get(raw_urim, stream=True)

    # warc_target_uri = None

    # # we have to implement this construct in case the archive combines original with other relations
    # for link in resp.links:

    #     if 'original' in link:
    #         warc_target_uri = resp.links[link]['url']

    # if warc_target_uri is None:
    #     module_logger.warning("could not find this memento's original resource, skipping {}".format(urim))
    #     return

    # try:
    #     mdt = resp.headers['Memento-Datetime']

    # except KeyError:
    #     print("could not find this memento's memento-datetime, skipping {}".format(urim))
    #     return

    # http_headers = StatusAndHeaders('200 OK',
    #     headers_list, protocol='HTTP/1.0')

    # module_logger.debug("mdt formatted by strptime and converted by strftime: {}".format(
    #     datetime.strptime(
    #         mdt, "%a, %d %b %Y %H:%M:%S GMT"
    #     ).strftime('%Y-%m-%dT%H:%M:%SZ')
    # ))       
    output_file = "rev-" + warc.split("/")[11]
    record_id, target_uri, date, http_headers = read_warc()
    #print(target_uri)
    parts =  target_uri.split("/p/")    
    target_uri_username = parts[0] + f"/{username}/p/" + parts[1]
    warc_headers_dict = {}
    warc_target_uri = target_uri_username
    warc_headers_dict['WARC-Refers-To'] = record_id
    warc_headers_dict['WARC-Refers-To-Target-URI'] = target_uri
    warc_headers_dict['WARC-Refers-To-Date'] = date
    warc_headers_dict['WARC-Profile'] = "http://netpreserve.org/warc/1.1/revisit/identical-payload-digest"
    warc_headers_dict['WARC-Date'] = date

    with open(f"{output_directory}/{output_file}", 'wb') as output:
        writer = WARCWriter(output, gzip=True)

        record = writer.create_warc_record(
            warc_target_uri, 'revisit',
            #payload=resp.raw,
            http_headers=http_headers,
            warc_headers_dict=warc_headers_dict
            )

        writer.write_record(record)


if __name__ == "__main__":
    # urim_list = [("http://web.archive.org/web/20150721221710/https://instagram.com/p/C/", "http://web.archive.org/web/20150721221710mp_/https://instagram.com/p/C/", ),
    #              ("http://web.archive.org/web/20160325025112/https://www.instagram.com/p/C/", "http://web.archive.org/web/20160325025112mp_/https://www.instagram.com/p/C/"),
    #              ("http://web.archive.org/web/20191026023931/https://www.instagram.com/p/C/","http://web.archive.org/web/20191026023931mp_/https://www.instagram.com/p/C/"),
    #              ("http://web.archive.org/web/20191025023618/https://instagram.com/p/D/", "http://web.archive.org/web/20191025023618mp_/https://instagram.com/p/D/"),
    #              ("http://web.archive.org/web/20210320085526/https://www.instagram.com/p/CEYmtQInzo9/", "http://web.archive.org/web/20210320085526mp_/https://www.instagram.com/p/CEYmtQInzo9/")
    #              ]
    # urim_list = [("http://web.archive.org/web/20201215154228/https://twitter.com/realDonaldTrump/status/1338871862315667456", "http://web.archive.org/web/20201215154228mp_/https://twitter.com/realDonaldTrump/status/1338871862315667456")]
    create_warc_revisit()
    # for each in urim_list:
    #     urim = each[0]
    #     raw_urim = each[1]
    #     create_warc(urim, raw_urim, output_directory)
