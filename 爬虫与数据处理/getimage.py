from bs4 import BeautifulSoup as Bsp
import threading
import Queue
import time
import urlparse
import urllib
import urllib2
import sys
import re
import os
from tqdm import tqdm
import json

cnt = 57515
for root, dirs, files in os.walk('shouji'):
    for f in tqdm(files):
        path = os.path.join(root, f)
        with open(path, 'r') as fin:
            js_file = json.load(fin, encoding='utf8')
        try:
            url = 'http:'+js_file['images'][0]
        except:
            continue
        _header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
        try:
            req = urllib2.Request(url=url, headers=_header)
            res = urllib2.urlopen(req).read()
        except:
            continue
        with open('images/{}.jpg'.format(cnt), 'wb') as fout:
            fout.write(res)
        with open('imgid2url.txt', 'a') as fout:
            fout.write('{} {}\n'.format(cnt, url))
        cnt += 1
        #if cnt == 500:
        #    break

reload(sys)
sys.setdefaultencoding('utf-8')