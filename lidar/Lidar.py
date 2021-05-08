import random
import json
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import math
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
        self.r_previous = ''

        self.temps1 = []
        self.temps2 = []

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

    def find_R_in_0(self,x,y):
        return math.sqrt(x**2+y**2)

    def faz_mo(self,x):
        fia = (15-x)/(15-5) if x>= 5 and x<=15 else 1 if x>=0 and x<5 else 0
        fib = 0 if x <= 10 else (x-10)/(30-10) if x < 30 and x > 10 else 1
        return fia, fib

    def faz_ex(self,x):
        fia = (0.3-x)/(0.3-0.1) if x>=0.2 and x<= 0.3 else 1 if x>=0 and x<0.2 else 0
        fib = (x-0.2)/(0.4-0.2) if x>=0.2 and x<= 0.4 else 0 if x<0.2 else 1
        return fia, fib

    def faz_moe(self,x):
        fia = (0.04-x)/(0.04-0.02) if x >=0.02 and x<=0.04 else 1 if x>=0 and x<0.02 else 0
        fib = (x-0.02)/(0.06-0.02) if x>=0.02 and x<=0.06 else 0 if x<0.02 else 1
        return fia,fib

    def faz_cnt_in(self,x):
        fia = (1 if x<=0.1 else 1-2*((x-0.1)/(0.3-0.1))**2
                if x>=0.1 and x<=(0.3+0.1)/2 else 2*((0.3-x)/(0.3-0.1))**2
                if x<=0.3 and x>=(0.3+0.1)/2 else 0)
        fic = 0 if x<=0.4 else (x-0.4)/(0.5-0.4) if x>=0.4 and x<=0.5 else (0.6-x)/(0.6-0.5) if x>=0.5 and x<=0.6 else 0
        fid = (0 if x<=0.5 else 2*((x-0.5)/(0.65-0.5))**2 if x>=0.5 and x<=(0.5+0.6)/2 else 1-2*((0.65-x)/(0.65-0.5))**2
                if x>=(0.5+0.65)/2 and x<=0.65 else 1-2*((x-0.65)/(0.8-0.65))**2 if x>=0.65 and x<=(0.65+0.8)/2
                else 2*((0.8-x)/(0.8-0.65))**2 if x>=(0.8+0.65)/2 and x<=0.8 else 0)
        fie = (0 if x<=0.7 else 2*((x-0.7)/(0.9-0.7))**2 if x>=0.7 and x<=(0.7+0.9)/2 else 1-2*((0.9-x)/(0.9-0.7))**2
                if x>=(0.7+0.9)/2 and x<=0.9 else 1)
        return fia,fic,fid,fie

    def faz_mic(self,x):
        fia = 1 if x<=2 else 1-2*((x-2)/(4-2))**2 if x>=2 and x<=(4+2)/2 else 2*((4-x)/(4-2))**2 if x>=(4+2)/2 and x<=4 else 0
        fib = 0 if x<=2 else 2*((x-2)/(4-2))**2 if x>=2 and x<=(4+2)/2 else 1-2*((4-x)/(4-2))**2 if x>=(4+2)/2 and x<=4 else 1
        return fia,fib

    def fazification(self,mo,moe,cnt_in,mic,ex):
        fi_mo_a, fi_mo_b = self.faz_mo(mo)
        fi_ex_a, fi_ex_b = self.faz_ex(ex)
        fi_moe_a, fi_moe_b = self.faz_moe(abs(moe))
        fi_cnt_a, fi_cnt_c, fi_cnt_d, fi_cnt_e = self.faz_cnt_in(cnt_in)
        fi_mic_a, fi_mic_b = self.faz_mic(mic)
        print(f"Функция принадлежности по мат ожиданию круга {fi_mo_a,fi_mo_b}")
        print(f"Функция принадлежности по экцентриситету {fi_ex_a,fi_ex_b}")
        print(f"Функция принадлежности по мат ожиданию эллипса {fi_moe_a,fi_moe_b}")
        print(f"Функция принадлежности по кол-ву точек внутри идеального круга {fi_cnt_a, fi_cnt_c, fi_cnt_d, fi_cnt_e}")
        print(f"Функция принадлежности по среднему отклонению от идеальной трубы {fi_mic_a, fi_mic_b}")
        fi_data = [[fi_mo_a,fi_mo_b],[fi_ex_a,fi_ex_b],[fi_moe_a,fi_moe_b],[fi_cnt_a,fi_cnt_c,fi_cnt_d,fi_cnt_e],[fi_mic_a,fi_mic_b]]
        self.defazification(fi_data)

    def defazification(self, fi):
        r = dict([('circle',0),('dent',0),('ellipse',0),('hydrate',0),('gaufrer',0)])
        r['circle'] = min(fi[0][0],fi[1][0],fi[2][0],fi[3][1],fi[4][0]) # Circle
        r['dent'] = min(fi[0][1],fi[1][1],fi[2][1],fi[3][2],fi[4][1]) # dent
        r['ellipse'] = min(fi[0][1],fi[1][1],fi[2][0],fi[3][1],fi[4][1]) # Ellipse
        r['hydrate'] = min(fi[0][0],fi[1][0],fi[2][0],fi[3][3],fi[4][1]) # Hydrate
        r['gaufrer'] = min(fi[0][0],fi[1][0],fi[2][0],max(fi[3][0],fi[3][3]),fi[4][1]) # Gaufrer
        #print(f"\nОтветы правил circle={r1}, dent={r2}, elipse={r3}, hydrate={r4}, gaufrer={r5}")
        #print(f"{r4==r5}")
        max1, max1s = r['circle'],'circle'
        print("\n")
        for key, value in r.items():
            print(f"Ответ правила {key} = {value}")
            #max1, max1s = (value,key) if value>max1 else pass
            if value>max1:
                max1, max1s = value, key
        #print(f"ANS = {max(r1,r2,r3,r4,r5)}\n")
        #print(f"ANS = {max1s,r[max1s]}")
        self.temps1.append(max1s) #TODO Разобраться с self.r_previous, ибо оно ошибочно!!!
        self.temps2.append(max1s)
        if len(self.r_previous) == 0:
            self.r_previous = max1s
        if len(self.temps1) >= 2:
            print(f"SHOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO {self.r_previous,self.temps2[-2]}")
        if self.r_previous == 'hydrate' and max1s == 'gaufrer':
            print(f"DA?????????????????????????????????????????????????? {self.r_previous, max1s, self.temps2[-2]}")
            self.r_previous = max1s
            self.temps2[-2] = max1s

        print(f"ANS = {max1s,max1}")
        return 0

    def correlation(self, list_data, rds):
        a = 0
        b = math.inf
        max1 = 0
        sum = 0
        min1 = math.inf
        cnt = 0
        incount = 0
        m_ic = 0
        m_ic_sum = 0
        for data in list_data:
            raz = data[0]**2 + data[1]**2 - rds**2
            sum += raz
            cnt += 1
            max1 = max(raz,max1)
            min1 = min(min1,raz)
            temp = self.find_R_in_0(data[0],data[1])
            a = max(a,temp)
            b = min(b,temp)
            if temp <= self.rds:
                incount += 1
            m_ic_sum += abs(temp-self.rds)
            #print(f"x={data[0]}, y={data[1]}, R={self.rds_mean}, raznica={raz}\n")
        mo, cnt_in, mic = sum/cnt, incount/cnt, m_ic_sum/cnt
        print(f"По кругу max={max1}, min={min1}, Мат. Ожид={mo},\n",
        f"кол-во точек внутри идеальной трубы(%):{cnt_in}\nСреднее отклонение от идеальной трубы = {mic}")
        raz = 0
        sum = 0
        for data in list_data:
            raz = data[0]**2/a**2+data[1]**2/b**2-1
            sum += raz
        moe, ex = sum/cnt, math.sqrt(1-b**2/a**2)
        print(f"По эллипсу a={a}, b={b}, Мат. Ожид={moe}",
        f"\nExentricitet={ex}, C={a*math.sqrt(1-b**2/a**2)}\n")
        self.fazification(mo,moe,cnt_in,mic,ex)

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
            list_data = []
            rds_mean = 0
            while self.angl<=360:
                temp_err = random.uniform(-self.err_rds,self.err_rds)
                x = (rds2 + temp_err) * cos(radians(self.angl))
                y = (rds2 + temp_err) * sin(radians(self.angl))
                self.draw(x,y,color=255)
                self.list_data.append([x,y,self.z,cnt])
                list_data.append([x,y])
                rds_mean += rds2 + temp_err
                #rds2 = self.rds + temp_err
                x = (self.rds + temp_err) * cos(radians(self.angl))
                y = (self.rds + temp_err) * sin(radians(self.angl))
                self.z += 1
                self.draw(x,y)
                self.angl+=self.step_angl
                cnt += 1
            #print("sr raduis",sr/cnt)
            self.correlation(list_data,rds_mean/cnt)
            #self.correlation_elip(list_data)
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
            list_data = []
            a = self.rds * (1+width_ellipse*(i+1))  if i < circles else self.rds * (1+width_ellipse*(circles*2-i-1))
            b = self.rds * (1-width_ellipse*(i+1)) if i < circles else self.rds * (1-width_ellipse*(circles*2-i-1))
            #print(f"i= {i} rds_hyd = {rds_hyd}")
            relips = 0
            while self.angl<=360:
                temp_err = random.uniform(-self.err_rds,self.err_rds)
                rdsa = a + temp_err
                rdsb = b + temp_err
                x = (rdsa) * cos(radians(self.angl))
                y = (rdsb) * sin(radians(self.angl))
                self.draw(x,y,color=255)
                self.list_data.append([x,y,self.z,cnt])
                relips += self.find_R_in_0(x,y)
                list_data.append([x,y])
                rds2 = self.rds + temp_err
                y = (rds2) * sin(radians(self.angl))
                x = (rds2) * cos(radians(self.angl))
                self.z += 1
                self.draw(x,y)
                self.angl+=self.step_angl
                cnt += 1
            #print("sr raduis",sr/cnt)
            self.correlation(list_data,relips/cnt)
            #self.correlation_elip(list_data)
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
            rds_mean = 0
            list_data = []
            while self.angl<=360:
                temp_err = random.uniform(-self.err_rds,self.err_rds)
                rds2 = rds_hyd + temp_err
                x = (rds2) * cos(radians(self.angl))
                y = (rds2) * sin(radians(self.angl))
                self.draw(x,y,color=255)
                self.list_data.append([x,y,self.z,cnt])
                list_data.append([x,y])
                rds_mean += rds2
                rds2 = self.rds + temp_err
                y = (rds2) * sin(radians(self.angl))
                x = (rds2) * cos(radians(self.angl))
                self.z += 1
                self.draw(x,y)
                self.angl+=self.step_angl
                cnt += 1
            #print("sr raduis",sr/cnt)
            self.correlation(list_data,rds_mean/cnt)
            #self.correlation_elip(list_data)
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
            cntr = 0
            rds_mean = 0
            list_data = []
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
                list_data.append([x,y])
                if self.rds_mean*(1-self.dent_threshold) < rds2:
                    self.draw(x,y)
                else:
                    self.draw(x,y,color=255)
                self.angl+=self.step_angl
                cnt += 1
                cntr += 1
                rds_mean += rds2
            #print("sr raduis",sr/cnt)
            cnt = 0
            rds_mean = rds_mean/cntr
            self.correlation(list_data,rds_mean)
            #self.correlation_elip(list_data)
            self.angl = 0
            #sr = 0
            self.show_img()
            self.blank_img()
        #return list_data

    def data_gen(self,circles): # Задается ли изначально радиус трубы?
        #img = create_img()
        self.blank_img()
        cnt = 0
        #sr = 0 #средний радиус
        for i in range(circles):
            tempb = True
            list_data = []
            #sr = 0
            temp = 0
            rds_mean = 0
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
                rds_mean += rds2
                self.list_data.append([x,y,self.z,cnt])
                list_data.append([x,y])
                self.draw(x,y)
                self.angl+=self.step_angl
                cnt += 1
                temp += self.find_R_in_0(x,y)
            self.rds_mean /= cnt
            print("sr raduis",self.rds_mean)
            print(f"staroe R{rds_mean/cnt}, function R={temp/cnt}")
            self.correlation(list_data,rds_mean/cnt)
            #self.correlation_elip(list_data)
            cnt = 0
            self.angl = 0


            self.show_img()
            self.blank_img()
        #return list_data,sr

    def data_gen_ideal(self,circles): # Задается ли изначально радиус трубы?
        self.blank_img()
        cnt = 0
        for i in range(circles):
            list_data = []
            rds_mean = 0
            while self.angl<=360:
                rds2 = self.rds
                x = (rds2) * cos(radians(self.angl))  #+ 400
                y = (rds2) * sin(radians(self.angl))  #+ 400
                self.z += 1
                self.rds_mean += rds2
                self.list_data.append([x,y,self.z,cnt])
                list_data.append([x,y])
                rds_mean += rds2
                self.draw(x,y)
                self.angl+=self.step_angl
                cnt += 1
            self.rds_mean /= cnt
            print("sr raduis",self.rds_mean)
            self.correlation(list_data,rds_mean/cnt)
            #self.correlation_elip(list_data)
            cnt = 0
            self.angl = 0

            self.show_img()
            self.blank_img()

circles = 3 # колво кругов
step_angl = 3 # шаг угла
rds = 200 # расстояние до поверхности
err_rds = 2 #ошибка измерения
dent_threshold = 0.02 # трешхолд вмятины
dent_max = 90 # маскимальная длина вмятины в градусах
step_depth = 2 #шаг вмятины
res = Lidar(circles,step_angl,rds,err_rds,dent_threshold,dent_max,step_depth)
print('\nIDEAL CIRCLE\n')
res.data_gen_ideal(circles = 3)
print('\nCIRCLE\n')
res.data_gen(circles = 3)
print('\nDENT\n')
res.data_gen_dent(circles = 6)
print('\nELLIPSE\n')
res.data_gen_ellipse(circles = 6)
print('\nHYDRATE\n')
res.data_gen_hydrate(circles = 6)
print('\nGAUFRER\n')
res.data_gen_gaufrer(circles = 6)
#res.data_gen_ideal(circles = 1)
#print(res.list_data)
#res.correlation()
print(f"Ответы обычные {res.temps1}")
print(f"Ответы исправленные {res.temps2}")
'''
res.data_gen_dent(circles = 3)
res.data_gen(circles = 3)
res.data_gen_hydrate(circles = 6)
res.data_gen(circles = 3)
res.data_gen_ellipse(circles = 6)
res.data_gen(circles = 3)
res.data_gen_gaufrer(circles = 6)
#print(res.list_data)
'''
