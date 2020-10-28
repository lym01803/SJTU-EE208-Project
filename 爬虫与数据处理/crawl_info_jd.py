import urllib
import os
import json
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0)\
			Gecko/20100101 Firefox/14.0.1'}

def get_text(Soup):
	for script in Soup(['script', 'style']):
		script.decompose()#rip it out
	# get text
	text = Soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	return text

def get_res(url, price):
	ans = {}
	url = 'https:' + url
	ans['price'] = price
	ans['url'] = url
	ans['price_num'] = float(price[1:]) if len(price) > 1 else 0
	req = urllib.request.Request(url=url, headers=header)
	response = urllib.request.urlopen(req, timeout=10)
	content = response.read()
	Soup = BeautifulSoup(content, 'html.parser')
	ans['comment'] = []
	ans['star'] = []
	for comm in Soup.find_all('div', {'class': 'o-topic'}):
		ans['comment'].append(comm.strong.a.string)
		star = int(comm.span.get('class', '')[1][-1])
		ans['star'].append(star)
	ans['images'] = []
	for img_spe in Soup.find_all('img', {'id': 'spec-img'}):
		#print(img_spe)
		ans['images'].append(img_spe.get('data-origin', ''))
	for Lh in Soup.find_all('ul', {'class': 'lh'}):
		#print(Lh)
		for img in Lh.find_all('li'):
			ans['images'].append(img.img.get('src', ''))
	for bd in Soup.find_all('ul', {'id': 'parameter-brand'}):
		ans['brand'] = bd.li.get('title', '')
	ans['parameter'] = []
	for para in Soup.find_all('ul', {'class': 'parameter2 p-parameter-list'}):
		for lis in para.find_all('li'):
			#print(lis)
			ct = lis.get('title', '')
			if lis.string:
				nt = lis.string.split('：')[0]
			else:
				nt = lis.a.string.split('：')[0]
			ans['parameter'].append('%s:%s' % (nt, ct))
	for para in Soup.find_all('div', {'class': 'Ptable-item'}):
		lis1 = []
		lis2 = []
		for dt in para.find_all('dt'):
			lis1.append(dt.string)
		for dd in para.find_all('dd'):
			if dd.get('class', '') != '':
				continue
			lis2.append(dd.string)
		for i in range(len(lis1)):
			#print(lis1[i], lis2[i])
			ans['parameter'].append('{}:{}'.format(lis1[i], lis2[i]))
	for Na in Soup.find_all('div', {'class': 'sku-name'}):
		if Na.string:
			ans['name'] = Na.string.strip()
		else:
			ans['name'] = Na.img.string.strip()
	ans['title'] = Soup.head.title.string
	#print(ans['title'])
	ans['text'] = get_text(Soup)
	ans['class'] = 'xiangji'
	#with open('test_ans.json', 'w', encoding='utf8') as Fout:
	#	Fout.write('%s' % json.dumps(ans, indent=4))
	return ans

if not os.path.exists('xiangji'):
	os.mkdir('xiangji')
'''
page = '//item.jd.com/55513659186.html'
get_res(page, '￥1000')
'''
'''
with open('xiangji/56398033239.json', 'w', encoding='utf8') as Fout:
	Fout.write(json.dumps(get_res('//item.jd.com/56398033239.html', '¥2899.00'), indent=4))
exit()
'''
with open('targetlinkstest.txt', 'r', encoding='utf8') as Fin:
	tot = 1
	for lin in Fin:
		try:
			url, price = lin.strip().split()
		except:
			continue
		itemid = url[14: -5]
		#print(url)
		print('No.%d : %s' % (tot, url))
		tot += 1
		if tot < 17058:
			continue
		with open('xiangji/%s.json' % itemid, 'w', encoding='utf8') as Fout:
			Fout.write(json.dumps(get_res(url, price), indent=4))

