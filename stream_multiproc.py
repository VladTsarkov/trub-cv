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

class Watcher(Process):
    
    def _init__(self, DIR, q):
        super(Watcher,self).__init__()
        self.DIR = DIR
        self.q = q
    
    def run(self):
        if (len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])>200):
            self.q.put("False")
        else:
            self.q.put("True")

class Stitching(Process):

    #def __init__(self,q,dst, qw):
    def __init__(self,q,dst):
        super(Stitching,self).__init__()
        self.q1 = q[0]
        self.q2 = q[1]
        self.dst1 = dst[0]
        self.dst2 = dst[1]
        #self.qw = qw

    def run(self):
        print(self.q1.empty())
        print(self.q2.empty())
        #images = ()
        while 1:   #TODO: this
            #if (self.qw.get()=="False"):
            #    break
            """
            while 1:
                #if not(self.q1.empty()) and not(self.q2.empty()):
                try:
                    img1 = self.q1.get()
                    img2 = self.q2.get()
                    print("TRUE ", file=sys.stderr)

                except:
                #else:
                    print("FALSE ", file=sys.stderr)
                    print(self.q1.empty())
                    print(self.q2.empty())
                    img1_ = self.Transform(img1[0], self.dst1)
                    img2_ = self.Transform(img2[0], self.dst2)
                    break
            """
            img1 = self.q1.get()
            img2 = self.q2.get()
            img1_ = self.Transform(img1[0], self.dst1)
            img2_ = self.Transform(img2[0], self.dst2)
            
            #cv.imwrite('/home/student/more_space/stitch/holst_%s.jpg' % time.time(),img1_+img2_)
            #img3 = img1+img2
            #cv.resize(img1_,(893,671))
            #cv.resize(img2_,(893,671))
            cv.imshow('video',img1_+img2_)
            
            cv.waitKey(1)
            #print(111111111111111111, file=sys.stderr)
        #img2 = q2.get()

    """
    def Transform(self, img, dst):
        src = np.array([
        [0, 0],
        [3008, 0],
        [3008, 3008],
        [0, 3008]], dtype = "float32")
        M = cv.getPerspectiveTransform(src, dst)
        warped = cv.warpPerspective(img, M, (5599, 4208))
        return warped
    """
    
    def Transform(self, img, dst):
        src = np.array([
        [0, 0],
        [480, 0],
        [480, 480],
        [0, 480]], dtype = "float32")
        M = cv.getPerspectiveTransform(src, dst)
        warped = cv.warpPerspective(img, M, (893, 671))
        return warped
    

class VideoReader(Process):

    #def __init__(self, ip, q, qw):
    def __init__(self, ip, q):
        super(VideoReader, self).__init__()
        self.ip = "rtsp://admin:admin@" + ip + ":554/ch01/2"
        #self.ip = "rtsp://admin:admin@" + ip + ":554/ch01/0"
        self.q = q
        #self.ip = ip
        #self.dst = dst
        #self.stream = VideoStream(self.ip).start()
        #self.stream = cv.VideoCapture(self.ip)
        #self.qw = qw

    def run(self):
        #stream = VideoStream(self.ip).start()
        stream = cv.VideoCapture(self.ip)
        #print(111111111111111111, file=sys.stderr)
        #if(self.stream.isOpened()==False):
        #    print('smth wrong')
        while(1):
            #if (self.qw.get()=="False"):
            #    break
            #frame = self.stream.read()
            #frame = stream.read()
            #print(222222, file=sys.stderr)
            #ret, frame = self.stream.read()
            ret, frame = stream.read()
            #print("RET? ", ret)
            time = datetime.datetime.now().time()
            #t=()
            t = (frame,time)
            self.q.put(t)
            #q.put(t)
            cv.imshow('video? ',frame)
            #print(frame,time)
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
"""
Cam168coord = np.array([
[454,200],
[878,167],
[893,655],
[384,636]], dtype = "float32")
Cam169coord = np.array([
[0,52],
[544,180],
[522,573],
[30,670]], dtype = "float32")

QWatcher = Queue()
QWatcher.put("True")
#print(QWatcher.get())
DIR = '/home/student/more_space/stitch'

jobs = []
IP = ("192.168.1.169","192.168.1.168")
COORDS = (Cam169coord, Cam168coord)
#p = VideoReader(t1,t2)
#Watcher(DIR, QWatcher).start()
Q = []
for ip in IP:
    q = Queue()
    #VideoReader(ip, q, QWatcher).start()
    VideoReader(ip, q).start()
    #p = VideoReader(ip, q)
    #jobs.append(p)
    #p.start()
    Q += [q]

#Stitching(Q, COORDS, QWatcher).start()
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
