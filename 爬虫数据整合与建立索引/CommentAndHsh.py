import os
import json
import re
from tqdm import *
import sys

reload(sys)
sys.setdefaultencoding('utf8')
Dir = sys.argv[1]
with open('score.json','r') as fin:
    score = json.load(fin,encoding = 'utf8')
with open('imgurl.json','r') as fin:
    hsh = json.load(fin,encoding = 'utf8')
for root, dirs, files in os.walk(Dir):
    for f in tqdm(files):
        path = os.path.join(root, f)
        try:
            with open(path, 'r') as fin:
                tmpjs = json.load(fin, encoding='utf8')
            
            id = tmpjs['id']
            tmpjs['rate'] = score[id]
            img = tmpjs['images'][0]
            img = img.lstrip('http://').lstrip('https://').lstrip('://')
            tmpjs['imghash'] = hsh[img]
                
        except:
            continue
        with open(path, 'w') as fout:
            json.dump(tmpjs, fout, ensure_ascii=False, indent=4)
