from frameseg import *
import cv2

flag = 0

def on_mouse(event, x, y, flags, param):
    global posx, posy, posx1, posy1, flag
    if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键按下
        if flag >= 1:
            posx1 = x
            posy1 = y
            # if flag == 1:  # 获取点击的第二点
            #     cv2.destroyAllWindows() # 关闭当前窗口
        else:
            posx = x
            posy = y
            # 获取鼠标点击的第一点
        flag += 1
        print(flag)
        print(posx,posy)
        print(posx1,posy1)

def exchange(x, y, x1, y1):
    if x > x1:
        x,x1 = x1,x
    if y > y1:
        y,y1 = y1,y
    return x,y,x1,y1

img = cv2.imread('02.png')
img = cv2.resize(img, (800,600),
                    interpolation=cv2.INTER_CUBIC)
img = frame_seg(img)
cv2.imshow('1', img)
cv2.setMouseCallback("1", on_mouse, 0)
cv2.waitKey(0)  # 用于给窗口提供展示时间
cv2.destroyAllWindows()