import cv2 as cv
# import cv
import imutils
from imutils.video import VideoStream
#from Transform import Transform
from multiprocessing import Process, Queue, Semaphore
import numpy as np
import time
import datetime
import sys
import os


class VideoWriter(Process):

    def __init__(self, ip, name, ch, stream,q):
        super(VideoWriter, self).__init__()
        self.ip = "rtsp://admin:admin@%s:554/%s/%s" % (ip, ch, stream)
        self.name = name

    def run(self):
        stream = cv.VideoCapture(self.ip)
        ret, frame = stream.read()
        #print(frame.shape)
        out = cv.VideoWriter(self.name, cv.VideoWriter_fourcc('M','J','P','G'), 25, frame.shape[0:2])
        while(q.get_value()==1):
            ret, frame = stream.read()
            
            if ret == True:
                out.write(frame)
                #print(dir(out))
                
                #cv.imshow('frames', frame)
                
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        out.release()
        stream.release()



q = Semaphore()
IP = ("192.168.1.168","192.168.1.169")
names = ("out.avi","out2.avi")
ch = "ch01"
stream=("1","1")
Q = []
for i in range(2):
    VideoWriter(IP[i],names[i],ch,stream[i], q).start()
    
#for ip in IP:
    #q = Queue()
    #VideoReader(ip, q, QWatcher).start()
    #VideoWriter(ip, names).start()
    #p = VideoReader(ip, q)
    #jobs.append(p)
    #p.start()
    #Q += [q]



time.sleep(100)
q.acquire()
