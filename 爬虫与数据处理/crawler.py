import urllib, urllib2, sys, re, os
from tqdm import tqdm
from bs4 import BeautifulSoup as BSp
import json
import jieba
import threading

STR1 = {'shouji':'30193816', 'bijiben':'30193816'}
STR2 = {'shouji':'021_0210199', 'bijiben':'021_0210199'}

def get_comment(id1, id2):
    global STR1, type
    str = id2
    while len(str) < 11:
        str = '0'+str
    url = 'https://review.suning.com/ajax/cluster_review_lists/general-{}-0000000{}-{}-total-1-default-10-----reviewList.htm?callback=reviewList'.format(STR1[type], str, id1)
    _header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
    req = urllib2.Request(url=url, headers=_header)
    content = urllib2.urlopen(req, timeout=3.0).read()
    #print(url)
    return re.findall(re.compile('content":"(.+?)"'), content)
    #for item in res:
    #    print(item)
    #return res

def get_price(id1, id2):
    global STR2, type
    str = id2
    while len(str) < 11:
        str = '0' + str
    url = 'https://icps.suning.com/icps-web/getVarnishAllPriceNoCache/0000000{}_{}_{}_1_getClusterPrice.jsonp?callback=getClusterPrice'.format(str, STR2[type], id1)
    _header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
    req = urllib2.Request(url=url, headers=_header)
    content = urllib2.urlopen(req, timeout=3.0).read()
    return re.findall(re.compile('price":"(.+?)"'), content)[0]

def get_img(img_str):
    img_str = img_str.replace('\n', ' ')
    tmp = re.findall(re.compile('images":(.+?)],'), img_str)[0]
    return re.findall(re.compile('"(.+?)"'), tmp)

def dealWithPage(url):
    global type
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
        img_str = bsp.find_all('script', attrs={'type':'application/ld+json'})[0].get_text()
        res['images'] = get_img(img_str)
        #res['images'] = []
        #for i in bsp.find_all('img', attrs={'id':'spec-img'}): # img id="spec-img"
        #    res['images'].append('https:'+i.get('data-origin'))
        #try:
        #    for i in bsp.find_all('ul', attrs={'class':'lh'})[0].find_all('li'):
        #        res['images'].append('https:'+i.img.get('src'))
        #except Exception, e:
        #    pass
        res['title'] = bsp.find_all('title')[0].get_text()
        P = bsp.find_all('div', attrs={'class':'name-inner'})
        res['brand'] = P[0].parent.parent.find_all('td')[1].a.get_text()
        res['parameter'] = []
        for item in P:
            pa = item.parent.parent.get_text().strip()
            res['parameter'].append(' '.join(jieba.cut(pa)))
        id1 = url.split('/')[-2]
        id2 = url.split('/')[-1].split('.')[0]
        res['comment'] = get_comment(id1, id2)
        res['price'] = get_price(id1, id2)
        res['class'] = type
        res['name'] = res['title']
        res['splitedname'] = ' '.join(jieba.cut(res['name']))
        for s in bsp(['script', 'style', 'head']):
            s.extract()
        res['text'] = ' '.join(jieba.cut(bsp.get_text()))
        name = url.split('/')[-1].split('.')[0]
        with open('{}/{}.json'.format(type, name), 'w') as fout:
            json.dump(res, fout, ensure_ascii=False, indent=4)
    except:
        pass

def adding_comment_and_price(url):
    global type
    name = url.split('/')[-1].split('.')[0]
    id1 = url.split('/')[-2]
    id2 = url.split('/')[-1].split('.')[0]
    try:
        with open('{}/{}.json'.format(type, name), 'r') as fin:
            tempjs = json.load(fin, encoding='utf8')
        tempjs['comment'] = get_comment(id1, id2)
        tempjs['price'] = get_price(id1, id2)
        with open('{}/{}.json'.format(type, name), 'w') as fout:
            json.dump(tempjs, fout, ensure_ascii=False, indent=4)
    except:
        return

def working(Id):
    global fin, total_cnt, numLimit
    while total_cnt < numLimit:
        if vlock.acquire():
            link = fin.readline()
            vlock.release()
            link = 'https:' + link.strip()
            #dealWithPage(link)
            adding_comment_and_price(link)
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

numLimit = 1600
total_cnt = 0
type = 'shouji'
fin = open('targetlinks_{}.txt'.format(type), 'r')
vlock = threading.Lock()
work()
fin.close()
#print get_price('0070094634', '11346320884')