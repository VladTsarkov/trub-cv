import cv2
import numpy as np
def Transform(img, x1,y1,x2,y2,x3,y3,x4,y4):
    dst = np.array([
    [x1,y1],
    [x2,y2],
    [x3,y3],
    [x4,y4]], dtype = "float32")
    src = np.array([
    [0, 0],
    [3008, 0],
    [3008, 3008],
    [0, 3008]], dtype = "float32")
    M = cv2.getPerspectiveTransform(src, dst)
    #warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    warped = cv2.warpPerspective(img, M, (5599, 4208))
    return warped
    #cv2.imwrite('holst.jpg',warped)

#imgHolst = cv2.imread('holst.jpg')
#imgNew2 = cv2.imread('New2.jpg')
#img1 = Transform(imgNew2, 0,324,3408,1131,3270,3588,188,4200)
#imgNew1 = cv2.imread('New1.jpg')
#img2 = Transform(imgNew1, 2844,1252,5500,1044,5599,4104,2404,3984)
#cv2.imwrite('holst.jpg',img1+img2)
#cv2.imwrite(imgHolst,img1)
#cv2.imwrite(imgHolst,img2)
