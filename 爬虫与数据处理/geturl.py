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

Set = set()

def geturls(page):
    global Set
    _header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
    req = urllib2.Request(url=page, headers=_header)
    content = ''
    try:
        content = urllib2.urlopen(req).read()
    except:
        pass
    bsp = Bsp(content, 'html.parser')
    for i in bsp.find_all('a', attrs={'class':'sellPoint'}):
        Set.add(i.get('href'))


for i in tqdm(range(150)):
    url = 'https://list.suning.com/0-258004-{}-{}.html'.format(i,i)
    geturls(url)

with open('targetlinks_bijiben.txt', 'w') as fout:
    for i in Set:
        fout.write('{}\n'.format(i))
