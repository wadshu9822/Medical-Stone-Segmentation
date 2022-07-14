from frameseg import *
import cv2

img = cv2.imread('01.png')
img = frame_seg(img)
cv2.imshow('1', img)
cv2.waitKey(0)  
cv2.destroyAllWindows()