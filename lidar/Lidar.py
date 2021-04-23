import random
import json
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import random
#import pandas as pd
from math import sin,cos,radians

class Lidar():
    def __init__(self,circles,step_angl,rds,err_rds,dent_threshold,dent_max,step_depth):
        self.list_data = []
        self.img = np.zeros((800,800,3),np.uint8)
        self.angl = 0
        self.z = 0
        self.circles = circles
        self.step_angl = step_angl
        self.rds = rds
        self.err_rds = err_rds
        self.rds_mean = 0
        self.dent_threshold = dent_threshold
        self.dent_max = dent_max
        self.depth = 0
        self.step_depth = step_depth

    def draw(self,x,y,color=0):
        cv.circle(self.img,(int(x+400),int(y+400)), 2, (0,0,color),-1)

    def show_img(self):
        cv.imshow('test',self.img)
        cv.waitKey(0)

    def blank_img(self):
        self.img[:] = (255,255,255)

    def create_img(self):
        self.img = np.zeros((800,800,3),np.uint8)
        self.blank_img()

    """def data_from_json(self,jsn):
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

        show_img(img)"""

    def data_gen_gaufrer(self,circles = 3): # Задается ли изначально радиус трубы?
        self.angl = 0
        cnt = 0
        #rds_hyd = self.rds
        #print(f"rds_hyd1 {rds_hyd}")
        width_gaufrer = random.uniform(30,70)
        a, b = self.rds, self.rds
        for i in range(circles):
            rds2 = self.rds + width_gaufrer if i%2 == 0 else self.rds - width_gaufrer
            #print(f"i= {i} rds_hyd = {rds_hyd}")
            while self.angl<=360:
                temp_err = random.uniform(-self.err_rds,self.err_rds)
                x = (rds2 + temp_err) * cos(radians(self.angl))
                y = (rds2 + temp_err) * sin(radians(self.angl))
                self.draw(x,y,color=255)
                self.list_data.append([x,y,self.z,cnt])
                #rds2 = self.rds + temp_err
                x = (self.rds + temp_err) * cos(radians(self.angl))
                y = (self.rds + temp_err) * sin(radians(self.angl))
                self.z += 1
                self.draw(x,y)
                self.angl+=self.step_angl
                cnt += 1
            #print("sr raduis",sr/cnt)
            cnt = 0
            self.angl = 0
            #sr = 0
            self.show_img()
            self.blank_img()

    def data_gen_ellipse(self,circles = 3): # Задается ли изначально радиус трубы?
        self.angl = 0
        cnt = 0
        #rds_hyd = self.rds
        #print(f"rds_hyd1 {rds_hyd}")
        width_ellipse = random.uniform(0.1,0.2)/circles
        a, b = self.rds, self.rds
        for i in range(circles*2):
            a = self.rds * (1+width_ellipse*(i+1))  if i < circles else self.rds * (1+width_ellipse*(circles*2-i-1))
            b = self.rds * (1-width_ellipse*(i+1)) if i < circles else self.rds * (1-width_ellipse*(circles*2-i-1))
            #print(f"i= {i} rds_hyd = {rds_hyd}")
            while self.angl<=360:
                temp_err = random.uniform(-self.err_rds,self.err_rds)
                rdsa = a + temp_err
                rdsb = b + temp_err
                x = (rdsa) * cos(radians(self.angl))
                y = (rdsb) * sin(radians(self.angl))
                self.draw(x,y,color=255)
                self.list_data.append([x,y,self.z,cnt])
                rds2 = self.rds + temp_err
                y = (rds2) * sin(radians(self.angl))
                x = (rds2) * cos(radians(self.angl))
                self.z += 1
                self.draw(x,y)
                self.angl+=self.step_angl
                cnt += 1
            #print("sr raduis",sr/cnt)
            cnt = 0
            self.angl = 0
            #sr = 0
            self.show_img()
            self.blank_img()

    def data_gen_hydrate(self,circles = 3): # Задается ли изначально радиус трубы?
        self.angl = 0
        cnt = 0
        rds_hyd = self.rds
        print(f"rds_hyd1 {rds_hyd}")
        width_hydrate = random.uniform(20,70)
        for i in range(circles*2):
            rds_hyd = rds_hyd-width_hydrate/circles if i < circles else rds_hyd+width_hydrate/circles
            print(f"i= {i} rds_hyd = {rds_hyd}")
            while self.angl<=360:
                temp_err = random.uniform(-self.err_rds,self.err_rds)
                rds2 = rds_hyd + temp_err
                x = (rds2) * cos(radians(self.angl))
                y = (rds2) * sin(radians(self.angl))
                self.draw(x,y,color=255)
                self.list_data.append([x,y,self.z,cnt])
                rds2 = self.rds + temp_err
                y = (rds2) * sin(radians(self.angl))
                x = (rds2) * cos(radians(self.angl))
                self.z += 1
                self.draw(x,y)
                self.angl+=self.step_angl
                cnt += 1
            #print("sr raduis",sr/cnt)
            cnt = 0
            self.angl = 0
            #sr = 0
            self.show_img()
            self.blank_img()

    def data_gen_dent(self,circles = 3): # Задается ли изначально радиус трубы?
        self.angl = 0
        cnt = 0
        for i in range(circles):
            angl_start_den = random.uniform(0,270)
            angl_end_den = angl_start_den + self.dent_max
            print(f"angl from {angl_start_den} into {angl_end_den}")
            while self.angl<=360:
                temp_err = random.uniform(-self.err_rds,self.err_rds)
                rds2 = self.rds + temp_err
                if self.angl>angl_start_den and self.angl<angl_end_den:
                    if self.angl<(angl_start_den+angl_end_den)/2:
                        self.depth += self.step_depth
                        rds2 -= self.depth
                        x = (rds2) * cos(radians(self.angl))  #+ 400
                        y = (rds2) * sin(radians(self.angl))  #+ 400
                    else:
                        self.depth -= self.step_depth
                        rds2 -= self.depth
                        x = (rds2) * cos(radians(self.angl))  #+ 400
                        y = (rds2) * sin(radians(self.angl))  #+ 400
                else:
                    x = (rds2) * cos(radians(self.angl))  #+ 400
                    y = (rds2) * sin(radians(self.angl))  #+ 400
                self.z += 1
                #sr += rds2
                self.list_data.append([x,y,self.z,cnt])
                #print(f"sr {sr*(1-threshold)} and rds {rds2}")
                if self.rds_mean*(1-self.dent_threshold) < rds2:
                    self.draw(x,y)
                else:
                    self.draw(x,y,color=255)
                self.angl+=self.step_angl
                cnt += 1
            #print("sr raduis",sr/cnt)
            cnt = 0
            self.angl = 0
            #sr = 0
            self.show_img()
            self.blank_img()
        #return list_data

    def data_gen(self,circles): # Задается ли изначально радиус трубы?
        #img = create_img()
        self.blank_img()
        cnt = 0
        #list_data = []
        #sr = 0 #средний радиус
        for i in range(circles):
            tempb = True
            #sr = 0
            while self.angl<=360:
                temp_err = random.uniform(-self.err_rds,self.err_rds)
                rds2 = self.rds + temp_err
                if not tempb:
                    rds2 += 100
                    tempb = False
                x = (rds2) * cos(radians(self.angl))  #+ 400
                y = (rds2) * sin(radians(self.angl))  #+ 400
                self.z += 1
                self.rds_mean += rds2
                self.list_data.append([x,y,self.z,cnt])
                self.draw(x,y)
                self.angl+=self.step_angl
                cnt += 1
            self.rds_mean /= cnt
            print("sr raduis",self.rds_mean)
            cnt = 0
            self.angl = 0

            self.show_img()
            self.blank_img()
        #return list_data,sr

circles = 3 # колво кругов
step_angl = 3 # шаг угла
rds = 200 # расстояние до поверхности
err_rds = 2 #ошибка измерения
dent_threshold = 0.02 # трешхолд вмятины
dent_max = 90 # маскимальная длина вмятины в градусах
step_depth = 2 #шаг вмятины
res = Lidar(circles,step_angl,rds,err_rds,dent_threshold,dent_max,step_depth)
res.data_gen(circles = 3)
res.data_gen_dent(circles = 3)
res.data_gen(circles = 3)
res.data_gen_hydrate(circles = 6)
res.data_gen(circles = 3)
res.data_gen_ellipse(circles = 6)
res.data_gen(circles = 3)
res.data_gen_gaufrer(circles = 6)
#print(res.list_data)
