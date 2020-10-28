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
        if tmpjs.get('parameter_nocut'):
            continue
        p = tmpjs['parameter']
        p2 = tmpjs['parameter']
        p = [i.decode('utf8') for i in p]
        try:
            if ('\xef\xbc\x9a' in p[0]):
                tmpjs['parameter'] = [i.split('\xef\xbc\x9a')[-1].encode('utf8').replace(' ','') for i in p]
                tmpjs['parameter_nocut'] = [':'.join(i.split('\xef\xbc\x9a')) for i in p]
                tmpjs['parameter'] = ' '.join(tmpjs['parameter'])
                tmpjs['parameter_nocut'] = '\n'.join(tmpjs['parameter_nocut']).encode('utf8')
            elif('       ' in p[0]):
                tmpjs['parameter'] = [i.split('       ')[-1].encode('utf8').replace(' ','') for i in p]
                tmpjs['parameter_nocut'] = [':'.join(i.split('       ')) for i in p]
                tmpjs['parameter'] = ' '.join(tmpjs['parameter'])
                tmpjs['parameter_nocut'] = '\n'.join(tmpjs['parameter_nocut']).encode('utf8')
            else:
                tmpjs['parameter'] = [i.split(':')[-1].encode('utf8') for i in p]
                tmpjs['parameter'] = ' '.join(tmpjs['parameter'])
                tmpjs['parameter_nocut'] = '\n'.join(p2)
				
        except:
            continue
        with open(path, 'w') as fout:
            json.dump(tmpjs, fout, ensure_ascii=False, indent=4)
