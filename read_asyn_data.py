from multiprocessing import Process, Queue, Semaphore, Value
import cv2 as cv
import json
import time

class DataGetVideo(Process):
    def __init__(self,name,data,val,q):
        super(DataGetVideo, self).__init__()
        self.name = name
        self.q = q
        self.val = val
        self.data = data
        self.count = 0

    def run(self):
        print("collecting data from ",self.name)
        #sem.acquire()
        stream = cv.VideoCapture(self.data)
        while 1:
            ret, frame = stream.read()
            #print("work")
            self.count+=1
            print("\tVIDEO ",self.count)
            self.val.value = True
            if ret == False:
                print("break")
                break
            if self.q.qsize() >= 2:
                self.q.get()
                self.q.put([frame,self.count])
            else:
                self.q.put([frame,self.count])
        stream.release()

class DataGetNav(Process):
    def __init__(self,name,data,val2,q2):
        super(DataGetNav, self).__init__()
        self.name = name
        self.q = q2
        self.val = val2
        self.data = data
        self.count = 0

    def run(self):
        print("collecting data from ",self.name)
        #sem.acquire()
        nav = json.load(open(self.data))
        for nav_data in nav:
            self.val.value = True
            self.count += 1
            print("Navigation ",self.count)
            if self.q.qsize() >= 2:
                self.q.get()
                self.q.put([nav_data,self.count])
            else:
                self.q.put([nav_data,self.count])

class DataGetLidar(Process):
    def __init__(self, name, data, val3, q3):
        super(DataGetLidar, self).__init__()
        self.name = name
        self.q = q3
        self.val = val3
        self.data = data
        self.count = 0

    def run(self):
        lidar = json.load(open(self.data))
        print("collecting data from %s, size data %s" %(self.name, len(lidar)))
        #sem.acquire()
        for item in lidar:
            self.val.value = True
            self.count += 1
            print("Lidar ",self.count)
            if self.q.qsize() >= 2:
                self.q.get()
                self.q.put([item,self.count])
            else:
                self.q.put([item,self.count])

class DataStruct(Process):
    def __init__(self, valV, valL, valN, Q):
        super(DataStruct, self).__init__()
        self.valV = valV
        self.valN = valN
        self.valL = valL
        self.qV = Q[0]
        self.qL = Q[1]
        self.qN = Q[2]

    def run(self):
        while 1:
            if self.valV.value and self.valN.value and self.valL.value:
                print("GOT NEW DATA")
                self.valV.value, self.valN.value, self.valL.value = False, False, False
                dataV = self.qV.get()
                dataN = self.qN.get()
                dataL = self.qL.get()
                print("Данные с камеры %s, данные с навигации %s, данные с лидара %s." %(dataV[1], dataN[1], dataL[1]))


valV = Value('b')
valL = Value('b')
valN = Value('b')
valV.value, valN.value, valL.value = False, False, False

nameV = "video"
nameL = "lidar"
nameN = "navigation"
dataV = "/home/tsar/python/trub-cv-new/trub-cv/img/out.avi"
#dataL = ['Это','другие','данные','да?','1?','2?','3?']
dataL = "/home/tsar/python/trub-cv-new/lidar/data/scan.json"
dataN = "/home/tsar/python/trub-cv-new/navigation/nav.json"
#DATA = [[name1,data],[name2,data2],[name3,data3]]

q, q2, q3 = Queue(), Queue(), Queue()
DataGetVideo(nameV,dataV,valV,q).start()
DataGetNav(nameN,dataN,valN,q3).start()
DataGetLidar(nameL,dataL,valL,q2).start()
Q = [q,q2,q3]
DataStruct(valV, valL, valN, Q).start()

'''for q in Q:
    q.close()
    q.join_thread()
'''
#print("SKOKA RAZ SEM",sem)
#time.sleep(100)
#sem.acquire()
