import cv2
import numpy as np
import os
import random
from tqdm import tqdm

def randomRotate(img, row, col, filename):
    p1 = np.float32([[col/2, row/2],[col/2+1, row/2],[col/2, row/2+1]])
    theta = random.uniform(0, 2*np.pi)
    p2 = np.float32([[col/2, row/2],[col/2+np.cos(theta), row/2+np.sin(theta)],[col/2-np.sin(theta),row/2+np.cos(theta)]])
    M = cv2.getAffineTransform(p1, p2)
    img_tmp = cv2.warpAffine(img, M, (col, row))
    cv2.imwrite(filename, img_tmp)

def randomColor(img):
    img2 = img + np.array([random.uniform(-100,100), random.uniform(-100,100), random.uniform(-100,100)])
    img2 = np.maximum(img2, 0)
    img2 = np.minimum(img2, 255)
    #cv2.imwrite('tmp.jpg', img2)
    return img2

def changeToSquare(img):
    x, y = img.shape[:2]
    if x < 0.75 * y :
        A = np.array(np.zeros((int((y-x)/2), y, 3)), dtype='uint8')
        B = np.array(np.zeros((int((y-x)/2), y, 3)), dtype='uint8')
        img = np.vstack((A,img,B))
    elif y < 0.75 * x:
        A = np.array(np.zeros((x, int((x-y)/2), 3)), dtype='uint8')
        B = np.array(np.zeros((x, int((x-y)/2), 3)), dtype='uint8')
        img = np.hstack((A,img,B))
    return img

filefolds = ["apple","CANON","dell","DJI","FUJIFILM","GoPro","hasee","HASSELBLAD","honor","hp","huashuo","huawei","Kodak","Leica","lenovo","LG","machenike","Manfrotto","meizu","microsoft","Newsmy","Nikon","nokia","nuoio","OLYMPUS","oppo","Panasonic","PENTAX","philips","realme","RICOH","SIGMA","SONY","sumsung","surface","Tamron","thinkpad","thunderobot","VILTROX","vivo","xiaomi","yijia","YONGNUO","Zeiss","ZTE"]

N = len(filefolds)
print(N)
suffix = '_ex'
for tag in range(N):
    fold = filefolds[tag]
    if not os.path.exists('{}{}'.format(fold, suffix)):
        os.mkdir('{}{}'.format(fold, suffix))
    for root, dir, files in os.walk(fold):
        for file in tqdm(files):
            try:
                filename = os.path.join(root, file)
                img = cv2.imread(filename, cv2.IMREAD_COLOR)
                #img = changeToSquare(img)
                filename = ''.join(file.split('.')[:-1])
                row, col = img.shape[:2]
                cv2.imwrite('{}{}/{}_0.jpg'.format(fold, suffix, filename), img)
                for i in range(5):
                    img2 = randomColor(img)
                    randomRotate(img2, row, col, '{}{}/{}_{}.jpg'.format(fold, suffix, filename, i+1))
            except:
                pass

