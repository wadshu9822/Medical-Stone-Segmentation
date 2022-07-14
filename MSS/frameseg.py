import cv2
import numpy as np


def gamma(img,gamma):
    b, g, r = cv2.split(img)
    b,g,r = b/255,g/255,r/255
    b = np.power(b,gamma)
    g = np.power(g,gamma)
    r = np.power(r,gamma)
    r = r * 255
    b = b * 255
    g = g * 255
    # ͨ����Ϊ0-255����������0-1�ĸ�����
    b = np.floor(b).round().astype(np.uint8)
    g = np.floor(g).round().astype(np.uint8)
    r = np.floor(r).round().astype(np.uint8)
    img = cv2.merge([b, g, r])
    return img
    
def frame_seg(input_img):
        # AREA
    area_left = 700
    area_right = 1250
    area_up = 300
    area_bottom = 800
    # avg G&B
    aB = 105.9
    aG = 157.4
    img = input_img
    # img =  img1[area_up:area_bottom, area_left:area_right,:]
    
    # img =  cv2.resize(img1, (400,400),
                            #    interpolation=cv2.INTER_CUBIC)
    # print(img1.shape)
    # img1 = gamma(img1,1.5)
    img= cv2.medianBlur(img,7)
    img= cv2.medianBlur(img, 5)
    # img= cv2.medianBlur(img, 5)



    B,G= img[:,:,0], img[:,:,1]
    B = 255-(np.abs(B-aB))
    G = 255-(np.abs(G-aG))
    B = B/255
    G = G/255
    B = np.power(B, 10)
    G = np.power(G, 10)
    B = B*255
    G = G*255

    B= cv2.blur(B, (25, 25))
    G= cv2.blur(G, (25, 25))

    Y =( 3*B +  G)/4

    Y = np.floor(Y).round().astype(np.uint8)
    Y= cv2.blur(Y, (25, 25))
    # Y= cv2.blur(Y, (25, 25))

    Y = Y/255
    Y = np.power(Y,3)
    Y = Y*255
    Y = np.floor(Y).round().astype(np.uint8)
    Y= cv2.blur(Y, (25, 25))
    # Y= cv2.blur(Y, (25, 25))



    ret,imgthresh = cv2.threshold(Y,0,255,
                cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)     #Otsu��ֵ����,ת��Ϊ��ֵͼ
    kernel = np.ones((3,3),np.uint8)                       #������̬�任�����
    imgopen = cv2.morphologyEx(imgthresh,cv2.MORPH_OPEN,
                kernel,iterations=2)                       #��̬�任��������
    imgbg = cv2.dilate(imgopen,kernel,iterations=3)        #���Ͳ�����ȷ������
    imgdist = cv2.distanceTransform(imgopen,cv2.DIST_L2,0) #����ת������ȥȷ��ǰ��
    ret,imgfg = cv2.threshold(imgdist,
                        0.7*imgdist.max(),255,2)           #�Ծ���ת�����������ֵ����
    imgfg = np.uint8(imgfg)                                #ת��Ϊ���������ǰ��
    ret,markers = cv2.connectedComponents(imgfg)           #�����ֵ������
    unknown = cv2.subtract(imgbg,imgfg)                    #ȷ��λ��δ֪����
    markers = markers + 1                                  #��1ʹ������Ϊ0
    markers[unknown == 255] = 0                            #��δ֪��������Ϊ0
    imgwater = cv2.watershed(img,markers)                  #ִ�з�ˮ���㷨�ָ�ͼ��
    img[imgwater == -1] = [0,255,0]                        #��ԭͼ�б���ǵ�����Ϊ��ɫ

    # cv2.imwrite(output_img,img1)
    return img