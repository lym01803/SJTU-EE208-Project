import urllib, urllib2, sys, re, os
from tqdm import tqdm
from bs4 import BeautifulSoup as BSp
import json
import jieba
import threading

def dealWithPage(url):
    _header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
    req = urllib2.Request(url=url, headers=_header)
    try:
        content = urllib2.urlopen(req, timeout=5.0).read()
    except Exception, e:
        return
    #with open('ttt.txt', 'w') as ff:
    #    ff.write(content)
    try:
        res = {}
        bsp = BSp(content, 'html.parser')
        res['url'] = url
        res['images'] = []
        for i in bsp.find_all('img', attrs={'id':'spec-img'}): # img id="spec-img"
            res['images'].append('https:'+i.get('data-origin'))
        try:
            for i in bsp.find_all('ul', attrs={'class':'lh'})[0].find_all('li'):
                res['images'].append('https:'+i.img.get('src'))
        except Exception, e:
            pass
        res['title'] = bsp.find_all('title')[0].get_text()
        P = bsp.find_all('div', attrs={'class':'p-parameter'})[0].find_all('ul')
        res['brand'] = P[0].li.get('title')
        res['parameter'] = []
        for item in P[1].find_all('li'):
            pa = item.get_text().strip()
            res['parameter'].append(' '.join(jieba.cut(pa)))
        res['comment'] = []
        for item in bsp.find_all('div', attrs={'id':'hidcomment'}):
            #print(item)
            #print(item.get_text())
            res['comment'].append(item.get_text())
        try:
            res['price'] = bsp.find_all('span', attrs={'class':'pricing'})[0].get_text()
        except Exception, e:
            try:
                res['price'] = bsp.find_all('span', attrs={'class':'p-price'})[0].get_text()
            except Exception, e:
                res['price'] = 'none'
        res['class'] = 'laptop'
        res['name'] = bsp.find_all('div', attrs={'class':'sku-name'})[0].get_text()
        res['splitedname'] = ' '.join(jieba.cut(res['name']))
        for s in bsp(['script', 'style', 'head']):
            s.extract()
        res['text'] = ' '.join(jieba.cut(bsp.get_text()))
        name = url.split('/')[-1].split('.')[0]
        with open('result2/{}.json'.format(name), 'w') as fout:
            json.dump(res, fout, ensure_ascii=False)
    except Exception, e:
        pass

def working(Id):
    global fin, total_cnt, numLimit
    while total_cnt < numLimit:
        if vlock.acquire():
            link = fin.readline()
            vlock.release()
            link = 'https:' + link.strip()
            dealWithPage(link)
            total_cnt += 1
            print('Thread: {}, Number: {}'.format(Id, total_cnt))

def work():
    Num = 16
    t = list()
    for i in range(Num):
        t.append(threading.Thread(target=working, args=(i+1,)))
        t[i].setDaemon(True)
        t[i].start()
    for i in range(Num):
        t[i].join()

reload(sys)
sys.setdefaultencoding('utf-8')

numLimit = 45000
total_cnt = 0
fin = open('targetlinks8.txt', 'r')
vlock = threading.Lock()
work()
fin.close()
