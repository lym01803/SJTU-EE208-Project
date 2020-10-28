import urllib, urllib2, sys, re, os
from tqdm import tqdm
from bs4 import BeautifulSoup as BSp

links = []

def getTargetLinks(page):
    global links
    url = "https://list.jd.com/list.html?cat=670,671,672&page={}&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main".format(page)
    _header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
    req = urllib2.Request(url=url, headers=_header)
    try:
        content = urllib2.urlopen(req, timeout=5.0).read()
    except Exception, e:
        return
    with open('htmlcode.txt', 'w') as fout:
        fout.write(content)
    bsp = BSp(content, 'html.parser')
    for item in bsp.find_all('li', attrs={'class':'gl-item'}):
        links.append(item.div.find_all('div', attrs={'class':'p-img'})[0].a.get('href'))


for st in range(2, 8):
    for i in tqdm(range(st*100, (st+1)*100)):
        getTargetLinks(i)
    with open('targetlinks{}.txt'.format(st+1), 'w') as fout:
        for item in links:
            fout.write('{}\n'.format(item))
    print(len(links))