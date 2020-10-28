import cv2
import re
import os
import numpy as np
from tqdm import tqdm
import pickle

res = list()
taglist = list()
filefolds = ["apple","CANON","dell","DJI","FUJIFILM","GoPro","hasee","HASSELBLAD","honor","hp","huashuo","huawei","Kodak","Leica","lenovo","LG","machenike","Manfrotto","meizu","microsoft","Newsmy","Nikon","nokia","nuoio","OLYMPUS","oppo","Panasonic","PENTAX","philips","realme","RICOH","SIGMA","SONY","sumsung","surface","Tamron","thinkpad","thunderobot","VILTROX","vivo","xiaomi","yijia","YONGNUO","Zeiss","ZTE"]
N = len(filefolds)
mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
sz = 32
for tag in range(N):
    fold = filefolds[tag]+'_ex'
    print(fold)
    for root, dir, files in os.walk(fold):
        for file in tqdm(files):
            filename = os.path.join(root, file)
            img = cv2.imread(filename, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (sz, sz), interpolation=cv2.INTER_CUBIC)
            img = np.array(img, dtype=np.float32)
            img = (img/255.0 - mean) / std
            img = img.transpose([2,0,1])
            taglist.append(tag)
            res.append(img)
res = np.stack((res), axis=0)
taglist = np.array(taglist, dtype='int')
print(res.shape)
print(taglist.shape)
print(taglist)
with open('traindata.p', 'wb') as fout:
    pickle.dump(res, fout)
with open('traintag.p', 'wb') as fout:
    pickle.dump(taglist, fout)
