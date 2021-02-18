import random
import json
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import random
#import pandas as pd
from math import sin,cos,radians
x_coordinates = []
y_coordinates = []
def show_img(img):
    cv.imshow('test',img)
    cv.waitKey(0)
    return 0
def blank_img(img):
    img[:] = (255,255,255)
def create_img():
    img = np.zeros((800,800,3),np.uint8)
    #img[:] = (255,255,255)
    blank_img(img)
    return img
def gen_coord():
    return 0
def data_from_json(jsn):
    data = json.load(open(jsn))
    print(data)
    st = 0.
    img = create_img()
    cnt = 0
    for trash, trash2, angl, rds in data:

        if rds != 0:
            '''if st > angl:
                print("krug ",st,angl)
            st = angl
            '''
        #TODO  Отсортировать по углам
            if st - angl > 300:
                print("\nnkrug\n ",st,angl,cnt)
                cnt = 0
                show_img(img)
                blank_img(img)
            st = angl
            cnt += 1
            x = rds * cos(radians(angl)) / 10 + 400
            y = rds * sin(radians(angl)) / 10 + 400
            cv.circle(img,(int(x),int(y)), 2, (0,0,0),-1)
            print(angl,rds,x,y)
    print(len(data))
    print(cnt)

    show_img(img)
def data_gen(circles=3,step_angl=3,rds=200,err_rds=2):
    angl = 0
    img = create_img()
    z = 0
    cnt = 0
    list_data = []
    for i in range(circles):
        while angl<=360:
            temp_err = random.uniform(-err_rds,err_rds)
            x = (rds+temp_err) * cos(radians(angl))  #+ 400
            y = (rds+temp_err) * sin(radians(angl))  #+ 400
            z += 1
            list_data.append([x,y,z,cnt])
            cv.circle(img,(int(x),int(y)), 2, (0,0,0),-1)
            angl+=step_angl
            cnt += 1
        cnt = 0
        angl = 0
        show_img(img)
        blank_img(img)
    return list_data
#data = json.loads()
"""with open('data/scan.json') as f:
    d = json.loads(f)
    print(d)
"""

'''data = pd.read_json('data/scan.json',lines=True)
print(data)
'''
jsn = 'data/scan-01.json'
#data_from_json(jsn)
list_data = data_gen()
print(list_data)
print(len(list_data))
