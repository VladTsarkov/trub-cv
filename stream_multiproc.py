import cv2 as cv
import imutils
from imutils.video import VideoStream
#from Transform import Transform
from multiprocessing import Process, Queue
import numpy as np
import time
import datetime
import sys

class Stitching(Process):

    def __init__(self,q,dst):
        super(Stitching,self).__init__()
        self.q1 = q[0]
        self.q2 = q[1]
        self.dst1 = dst[0]
        self.dst2 = dst[1]

    def run(self):
        #images = ()
         while 1:   #TODO: this
            while 1:
                """
                try:
                    x = 0; img1 = self.q1.get()
                    x = 1; img2 = self.q2.get()
                except ...
                """
                if !(self.q1.empty()):
                    img1 = self.q1.get()
             try:
                    img1 = ; x = 0
                    img2 = self.q2.get(); x = 1
                    #img1 = self.q1.get()
                    #img2 = self.q2.get()
                    img1_ = self.Transform(img1[0], self.dst1)
                    img2_ = self.Transform(img2[0], self.dst2)
                    cv.imwrite('/home/student/more_space/stitch/holst_%s.jpg' % time.time(),img1_+img2_)
                    #print(111111111111111111, file=sys.stderr)
             except LookupError: #??
                 break
        #img2 = q2.get()

    def Transform(self, img, dst):
        src = np.array([
        [0, 0],
        [3008, 0],
        [3008, 3008],
        [0, 3008]], dtype = "float32")
        M = cv.getPerspectiveTransform(src, dst)
        warped = cv.warpPerspective(img, M, (5599, 4208))
        return warped


class VideoReader(Process):

    def __init__(self, ip, q):
        super(VideoReader, self).__init__()
        self.ip = "rtsp://admin:admin@" + ip + ":554/ch01/0"
        #self.ip = ip
        #self.dst = dst
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

jobs = []
IP = ("192.168.1.169","192.168.1.168")
COORDS = (Cam169coord, Cam168coord)
#p = VideoReader(t1,t2)
Q = []
for ip in IP:
    q = Queue()
    VideoReader(ip, q).start()
    #p = VideoReader(ip, q)
    #jobs.append(p)
    #p.start()
    Q += [q]

Stitching(Q, COORDS).start()
#sp = Stitching(Q, COORDS)



while (1):
    time.sleep(1)

# cam1Q = Queue()
# cam2Q = Queue()
# stitchQ = Queue()
# p = VideoReader("192.168.1.169", cam1Q)
# p = VideoReader2("192.168.1.168", cam2Q)

#p.start()
#p.join()

"""
proc = []
for i in range(2):
    p = Process(target=VideoReader, args=(t1[i],t2[i]))
    p.start()
    proc+=[p]
for i in proc:
    i.join()
"""
