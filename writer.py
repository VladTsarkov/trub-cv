import cv2 as cv
import imutils
from imutils.video import VideoStream
from transform import Transform

import time

#vcap168 = cv.VideoCapture("rtsp://admin:admin@192.168.1.168:554/ch01/2")
vcap169 = cv.VideoCapture("rtsp://admin:admin@192.168.1.169:554/ch01/2")
out = cv.VideoWriter('out.avi', cv.VideoWriter_fourcc('M','J','P','G'), 10, (480, 480))
#out2 = cv.VideoWriter('out2.avi', cv.VideoWriter_fourcc('M','J','P','G'), 10, (480, 480))
while(1):
    #ret168,frame168 = vcap168.read()
    ret169,frame169 = vcap169.read()
    
    if ret169 == True:
        out.write(frame169)
        
        cv.imshow('frames', frame169)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    
    #cv.imshow('VIDEO', img1+img2)
    #break
    #cv.waitKey(1)

vcap169.release()
out.release()
cv.destroyAllWindows()