import cv2 as cv
import imutils
from imutils.video import VideoStream
from Transform import Transform
from multiprocessing import Process, Queue
import numpy as np
import time
import datetime

class Stitching(Process):
    def __init__(self,q1,q2):
        super(Stitching,self).__init__()
    def run(self):
        img1 = q1.get()
        img2 = q2.get()
        cv.imwrite('holst.jpg',img1+img2)
    def Transform(self, img):
        src = np.array([
        [0, 0],
        [3008, 0],
        [3008, 3008],
        [0, 3008]], dtype = "float32")
        M = cv2.getPerspectiveTransform(src, self.dst)
        warped = cv2.warpPerspective(img, M, (5599, 4208))
        return warped

class VideReader(Process):
    def __init__(self, ip, dst):
        super(VideReader, self).__init__()
        self.ip = "rtsp://admin:admin@" + ip + ":554/ch01/0"
        self.dst = dst
        self.stream = VideoStream(self.ip).start()
    def run(self):
        while(1):
            frame = self.stream.read()
            time = datetime.datetime.now().time()
            t = (frame,time)
            q.put(t)
            #img = self.Transform(frame)
            cv.waitKey(1)
"""
    def Transform(self, img):
        src = np.array([
        [0, 0],
        [3008, 0],
        [3008, 3008],
        [0, 3008]], dtype = "float32")
        M = cv2.getPerspectiveTransform(src, self.dst)
        warped = cv2.warpPerspective(img, M, (5599, 4208))
        return warped
"""
"""
class VideoReader:
    def __init__(self, ip, dst):
        self.ip = "rtsp://admin:admin@" + ip + ":554/ch01/0"
        #self.img = img
        self.dst = dst
        self.reader()
    def reader(self):
        stream = VideoStream(self.ip).start()
        while(1):
            frame = stream.read()
            img = self.Transform(frame)
            cv.waitKey(1)
    def Transform(self,img):
        src = np.array([
        [0, 0],
        [3008, 0],
        [3008, 3008],
        [0, 3008]], dtype = "float32")
        M = cv2.getPerspectiveTransform(src, self.dst)
        #warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
        warped = cv2.warpPerspective(img, M, (5599, 4208))
        return warped
"""

"""
        vcap168 = VideoStream(self.ip).start()
        while(1):
            frame168  = vcap168.read()
            cv.imshow('1',frame168)
            cv.waitKey(1)
"""

"""
Cam168coord = np.array([
[2844,1252],
[5500,1044],
[5599,4104],
[2404,3984]], dtype = "float32")
Cam169coord = np.array([
[0,324],
[3408,1131],
[3270,3588],
[188,4200]], dtype = "float32")
t1 = ("192.168.1.169","192.168.1.168")
t2 = (Cam169coord, Cam168coord)
p = ProcessVideReader(t1,t2)
p.start()
p.join()
"""

time = datetime.datetime.now().time()
print(time)

"""
proc = []
for i in range(2):
    p = Process(target=VideoReader, args=(t1[i],t2[i]))
    p.start()
    proc+=[p]
for i in proc:
    i.join()
"""
