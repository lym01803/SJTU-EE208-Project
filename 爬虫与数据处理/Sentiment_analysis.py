import json
import os
from snownlp import SnowNLP
from tqdm import tqdm

def f(x):
	return x ** 1.4

def scoring(comments):
	if len(comments) == 0:
		return 20
	stand = f(1)
	scores = []
	for com in comments:
		S = SnowNLP(u'%s' % com)
		scores.append(S.sentiments)
		#print(S.sentiments, com)
	scores = [max(0.05, f(i) / stand) for i in scores]
	return sum(scores) / len(scores) * 100

namelist = []
with open('namelist.txt', 'r') as Fin:
	for lin in Fin:
		if lin.find('json') == -1:
			continue
		namelist.append(lin.strip())
if not os.path.exists('../tot_new'):
	os.mkdir('../tot_new')

for names in tqdm(namelist):
	info = {}
	with open(names, 'r', encoding='utf8') as Fin:
		info = json.load(Fin)
		info['comment_score'] = scoring(info['comment'])
	with open('../tot_new/%s' % names, 'w', encoding='utf8') as Fout:
		Fout.write(json.dumps(info, indent=4))
