import os
import json
import re
from tqdm import *
import sys

reload(sys)
sys.setdefaultencoding('utf8')
Dir = sys.argv[1]
for root, dirs, files in os.walk(Dir):
    for f in tqdm(files):
        path = os.path.join(root, f)
        with open(path, 'r') as fin:
            tmpjs = json.load(fin, encoding='utf8')
        try:
            if len(tmpjs['comment']) ==1:
                tmpjs['comment'] = tmpjs['comment'][0].split('\n\n\n')
            tmpjs['comment'] = [i.strip('\n').strip('()') for i in tmpjs['comment']]
            if "jd" in Dir:
                tmpjs['platform'] = 'jd'
            elif "sn" in Dir:
                tmpjs['platform'] = 'sn'
            tmpjs['id'] = f.rstrip('.json')
            if tmpjs.get('price_num'):
                tmpjs['price'] = str(tmpjs['price_num'])
            tmpjs['lower_title'] = tmpjs['title'].lower().strip()
            tmpjs['lower_name'] = tmpjs['name'].lower().strip()
        except Exception as e:
            print e
        total_pth = os.path.join('/media/EE/Final', 'total')
        if not os.path.exists(total_pth):
            os.mkdir(total_pth)
        with open(os.path.join(total_pth,f), 'w') as fout:
            json.dump(tmpjs, fout, ensure_ascii=False, indent=4)
