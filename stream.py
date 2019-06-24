import cv2 as cv
import imutils
from imutils.video import VideoStream
from transform import Transform

import time
#vcap = cv.VideoCapture("rtsp://192.168.1.168:554/ch01/0")
#vcap = cv.VideoCapture("rtsp://192.168.1.168:554/ch00")

vcap168 = cv.VideoCapture("rtsp://admin:admin@192.168.1.168:554/ch01/2")
vcap169 = cv.VideoCapture("rtsp://admin:admin@192.168.1.169:554/ch01/2")

#vcap168 = VideoStream("rtsp://admin:admin@192.168.1.168:554/ch01/2").start()
#vcap169 = VideoStream("rtsp://admin:admin@192.168.1.169:554/ch01/2").start()

while(1):
    ret168,frame168 = vcap168.read()
    ret169,frame169 = vcap169.read()
    
    #frame168 = vcap168.read()
    #frame169 = vcap169.read()
    #time.sleep(0.5)

    """
    #просмотр двух камер
    frame168 = imutils.resize(frame168, width=400)
    frame169 = imutils.resize(frame169, width=400)
    cv.imshow('video1', frame168)
    cv.imshow('video2', frame169)
    """

    #cv.imwrite("New1.jpg",frame168)
    #cv.imwrite("New2.jpg",frame169)


    #сшивка через файл
    #img1 = Transform(frame169, 0,324,3408,1131,3270,3588,188,4200)
    #img2 = Transform(frame168, 2844,1252,5500,1044,5599,4104,2404,3984)
    
    img2 = Transform(frame168, 454,200,878,167,893,655,384,636)
    img1 = Transform(frame169, 0,52,544,180,522,573,30,670)
    #cv.imwrite('holst.jpg',img1+img2)


    cv.imshow('VIDEO', img1+img2)
    #break
    cv.waitKey(1)
