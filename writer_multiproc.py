import cv2 as cv
# import cv
import imutils
from imutils.video import VideoStream
#from Transform import Transform
from multiprocessing import Process, Queue
import numpy as np
import time
import datetime
import sys
import os


class VideoWriter(Process):

    def __init__(self, ip, name):
        super(VideoWriter, self).__init__()
        self.ip = "rtsp://admin:admin@" + ip + ":554/ch01/2"
        self.name = name

    def run(self):
        stream = cv.VideoCapture(self.ip)
        out = cv.VideoWriter(self.name, cv.VideoWriter_fourcc('M','J','P','G'), 10, (480, 480))
        while(1):
            ret, frame = stream.read()
            
            if ret == True:
                out.write(frame)
                
                cv.imshow('frames', frame)
                
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break




IP = ("192.168.1.169","192.168.1.168")
names = ("out.avi","out2.avi")

Q = []
for i in range(2):
    VideoWriter(IP[i],names[i]).start()
    
#for ip in IP:
    #q = Queue()
    #VideoReader(ip, q, QWatcher).start()
    #VideoWriter(ip, names).start()
    #p = VideoReader(ip, q)
    #jobs.append(p)
    #p.start()
    #Q += [q]




while (1):
    time.sleep(1)

