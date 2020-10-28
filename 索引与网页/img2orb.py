import cv2
import numpy as np
import os
from tqdm import tqdm

def geth(i, des):
    col = i >> 3
    return int((des[col]//28) + (col << 3) > i)

K = [
        [210, 243, 150, 88, 80, 151, 58, 106, 205, 6, 143, 41, 84, 23, 85, 5, 182, 20, 36, 50, 241, 11, 77, 51,],
        [82, 196, 160, 227, 57, 131, 5, 15, 7, 206, 8, 85, 24, 142, 150, 144, 203, 23, 129, 183, 106, 143, 186, 138,] ,
        [190, 134, 240, 184, 205, 96, 128, 236, 28, 31, 170, 70, 158, 124, 131, 19, 241, 249, 232, 156, 109, 43, 226, 211,],
    ]

toread = 'images'
tosave = 'hsh'

def calc_hash(des):
    res = []
    num = des.shape[0]
    for i in range(num):
        for k in K:
            hsh = 0
            for kk in range(len(k)):
                hsh ^= (geth(k[kk], des[i]) << kk)
            res.append(hsh)
    return res

detector = cv2.ORB_create(300)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
if __name__ == '__main__':
    for root, dirs, files in os.walk(toread):
        for f in tqdm(files):
            filename = os.path.join(root, f)
            img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            kp, des = detector.detectAndCompute(img, None)
            hsh = calc_hash(des)
            with open('{}/{}.txt'.format(tosave, '.'.join(f.split('.')[:-1])), 'w') as fout:
                for item in hsh:
                    fout.write('{} '.format(item))
