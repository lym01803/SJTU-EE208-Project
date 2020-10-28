import web
from web import form
import urllib2
import os
import lucene
import SearchFiles_html as sf
import cv2
import numpy as np
import img2orb
import baidu
from models import resnet20
import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, TensorDataset
import torchvision
import torchvision.transforms as transforms
import sys

urls = (
    '/', 'index',
    '/s', 's',
    '/img', 'img',
    '/si', 'si'
)
try:
    vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
except:
    vm_env = lucene.getVMEnv()

'''
init model
'''
model = resnet20(54)
restore_model_path = 'ckpt_3399_acc_0.923210.pth'
model.load_state_dict(torch.load(restore_model_path, map_location=torch.device('cpu'))['net'])
model.eval()
brandlist = ['apple','CANON', 'checky', 'dell', 'DJI', 'FUJIFILM',\
             'GoPro', 'hasee', 'HASSELBLAD', 'honor', 'hp', 'huashuo', \
             'huawei', 'JARAY', 'Kamlan', 'Kodak', 'LAOWA', 'Leica', \
             'lenovo', 'LG', 'machenike', 'Manfrotto', 'meitu', 'meizu',\
             'microsoft', 'Newsmy', 'Nikon', 'nokia', 'nuoio', 'OLYMPUS',\
             'oppo', 'Panasonic', 'PENTAX', 'philips', 'Polaroid', 'raytine',\
             'realme', 'RICOH', 'SAMSUNG', 'SIGMA', 'SONY', 'sumsung', 'surface',\
             'Tamron', 'thinkpad', 'thunderobot', 'tianyu', 'VILTROX', 'vivo',\
             'xiaomi', 'yijia', 'YONGNUO', 'Zeiss', 'ZTE']
mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
imgsz = 64
'''
init baidu tool
'''
APP_ID = '18241180'
API_KEY = 'bMy96yjZgd60hlxy18RK1IxU'
SECRET_KEY = 'VF945GTaYuHLgc0lWOfIuToVGF2vWXt7'
baiduObj = baidu.baiduApi(APP_ID, API_KEY, SECRET_KEY)


render = web.template.render('templates') # your templates

class index:
    def GET(self):
        return render.index(0)

class img:
    def GET(self):
        return render.index_img(0)

class s:
    def GET(self):
        user_data = web.input()
        try:
            order = int(user_data.order)
        except:
            order = 1
        vm_env.attachCurrentThread()
        a = [user_data.message]
        a += sf.retrieve(user_data.message, order)
        a += [order]
        return render.result(a)

class si:
    def POST(self):
        wbipt = web.input()
        vm_env.attachCurrentThread()
        if wbipt.way == '0':
            imgfile = wbipt.file
            with open('tempsave.jpg', 'wb') as fout:
                fout.write(imgfile)
            img = np.asarray(bytearray(imgfile), dtype='uint8')
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (imgsz, imgsz), interpolation=cv2.INTER_CUBIC)
            img = np.array(img, dtype=np.float32)
            img = (img / 255.0 - mean) / std
            img = img.transpose([2, 0, 1])
            input = torch.from_numpy(np.array([img]))
            outputs = model(input)
            _, predicted = outputs.max(1)
            searchstr = brandlist[predicted[0]]
            baiduRes = baiduObj.getWordFromImage2('tempsave.jpg')
            wdlist = baiduRes['words_result']
            for i in wdlist:
                if i != None:
                    #print(i)
                    if i['probability']['min'] > 0.99:
                        searchstr += " {}".format(i['words'])
            result = ["Logo"]
            result += sf.retrieve(searchstr, 1)
            return render.result_img(result)
        if wbipt.way == '1':
            imgfile = wbipt.file
            img = np.asarray(bytearray(imgfile), dtype='uint8')
            img = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
            kp, des = img2orb.detector.detectAndCompute(img, None)
            hsh = img2orb.calc_hash(des)
            searchstr = ' '.join([str(i) for i in hsh])
            result = ["Picture"]
            result += sf.retrieve_img(searchstr)
            return render.result_img(result)
        return render.result_img(["Failed To Search"])

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    app = web.application(urls, globals())
    app.run()
