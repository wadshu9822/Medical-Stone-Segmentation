from re import A
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
    
def exchange(ax, ay, ax1, ay1):
    x = ax; y = ay; x1 = ax1; y1 = ay1
    # print(type(y))
    # print(type(y1))
    if x > x1:
        x,x1 = x1,x
    if y > y1:
        y,y1 = y1,y
    return x,y,x1,y1

# def frame_seg(input_img, xcoordinate, ycoordinate):
#         # AREA
#     x0 = 500
#     x1 = 550
#     y0 = 300
#     y1 = 350
#     # avg G&B
#     aB = 105.9
#     aG = 157.4
#     aR = 50
#     img = input_img
#     # cv2.imshow('1',img)
#     # cv2.waitKey(0)  # ���ڸ������ṩչʾʱ��
#     # cv2.destroyAllWindows()
#     if len(xcoordinate)>=2:
#         x = xcoordinate
#         y = ycoordinate
#     # print(type(y))
#         x0 = x[-1]; x1 = x[-2]
#         y0 = y[-1]; y1 = y[-2]
#     # print(type(y0))
#     posx,posy,posx1,posy1 = exchange(x0,y0,x1,y1)
#     aB = np.average(img[posy:posy1, posx:posx1, 2])  # ��ȡͼ�� �߶ȣ���ȣ�ͨ��
#     aG = np.average(img[posy:posy1, posx:posx1, 1])
#     aR = np.average(img[posy:posy1, posx:posx1, 0])

    
    
#     # img =  img1[area_up:area_bottom, area_left:area_right,:]
    
#     # img =  cv2.resize(img1, (400,400),
#                             #    interpolation=cv2.INTER_CUBIC)
#     # print(img.shape)
#     # img1 = gamma(img1,1.5)
#     img= cv2.medianBlur(img,7)
#     img= cv2.medianBlur(img, 5)
#     # img= cv2.medianBlur(img, 5)



#     B,G,R= img[:,:,2], img[:,:,1], img[:,:,0]  # ����ʱΪRGB˳��
    
#     B = 255-(np.abs(B-aB))
#     G = 255-(np.abs(G-aG))
#     R = 255-(np.abs(R-aR))
#     B = B/255
#     G = G/255
#     R = R/255
#     B = np.power(B, 10)
#     G = np.power(G, 10)
#     R = np.power(R, 20)
#     B = B*255
#     G = G*255
#     R = R*255

#     B= cv2.blur(B, (25, 25))
#     G= cv2.blur(G, (25, 25))
#     R = cv2.blur(R, (25, 25))

#     if aB < 50:
#         Y = (4*B+G)/5  # B��Gͨ���ϳ�
#     else:
#         Y = (4*R + G)/5

#     Y = np.floor(Y).round().astype(np.uint8)
#     Y= cv2.blur(Y, (25, 25))
#     # Y= cv2.blur(Y, (25, 25))

#     Y = Y/255
#     Y = np.power(Y,3)
#     Y = Y*255
#     Y = np.floor(Y).round().astype(np.uint8)
#     Y= cv2.blur(Y, (25, 25))
#     # Y= cv2.blur(Y, (25, 25))



#     ret,imgthresh = cv2.threshold(Y,0,255,
#                 cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)     #Otsu��ֵ����,ת��Ϊ��ֵͼ
#     kernel = np.ones((3,3),np.uint8)                       #������̬�任�����
#     imgopen = cv2.morphologyEx(imgthresh,cv2.MORPH_OPEN,
#                 kernel,iterations=2)                       #��̬�任��������
#     imgbg = cv2.dilate(imgopen,kernel,iterations=3)        #���Ͳ�����ȷ������
#     imgdist = cv2.distanceTransform(imgopen,cv2.DIST_L2,0) #����ת������ȥȷ��ǰ��
#     ret,imgfg = cv2.threshold(imgdist,
#                         0.7*imgdist.max(),255,2)           #�Ծ���ת�����������ֵ����
#     imgfg = np.uint8(imgfg)                                #ת��Ϊ���������ǰ��
#     ret,markers = cv2.connectedComponents(imgfg)           #�����ֵ������
#     unknown = cv2.subtract(imgbg,imgfg)                    #ȷ��λ��δ֪����
#     markers = markers + 1                                  #��1ʹ������Ϊ0
#     markers[unknown == 255] = 0                            #��δ֪��������Ϊ0
#     imgwater = cv2.watershed(img,markers)                  #ִ�з�ˮ���㷨�ָ�ͼ��
#     img[imgwater == -1] = [0,255,0]                        #��ԭͼ�б���ǵ�����Ϊ��ɫ

#     # cv2.imwrite(output_img,img1)
#     return img

def frame_seg(input_img, xcoordinate, ycoordinate):
        # AREA
    x0 = 340
    x1 = 360
    y0 = 300
    y1 = 375
    # avg G&B
    aB = 105.9
    aG = 157.4
    aR = 50
    img = input_img
    # cv2.imshow('1',img)
    # cv2.waitKey(0)  # ���ڸ������ṩչʾʱ��
    # cv2.destroyAllWindows()
    if len(xcoordinate)>=2:
        x = xcoordinate
        y = ycoordinate
        # print(type(y))
        x0 = x[0]; x1 = x[1]
        y0 = y[0]; y1 = y[1]
    # print(type(y0))
    posx,posy,posx1,posy1 = exchange(x0,y0,x1,y1)
     # ��ȡͼ�� �߶ȣ���ȣ�ͨ��

    aR = np.average(img[posy:posy1, posx:posx1, 0])
    aG = np.average(img[posy:posy1, posx:posx1, 1])
    aB = np.average(img[posy:posy1, posx:posx1, 2])
    
    B, G, R = img[:, :, 2], img[:, :, 1], img[:, :, 0]
    
    R = np.floor(R).round().astype(np.uint8)  # floor round����ȡ��
    G = np.floor(G).round().astype(np.uint8)
    B = np.floor(B).round().astype(np.uint8)
    # ��ɫ�ͻ�ɫΪ����ɫ����ɫЧ��������
    # plotRGB(R,G,B)
    B = 255-(np.abs(B-aB))
    G = 255-(np.abs(G-aG))
    R = 255-(np.abs(R-aR))
    # plotRGB(R,G,B)
    # �Ը�ͨ�����й�һ��
    B = B/255
    G = G/255
    R = R/255

    # ��ǿ��������������
    B = np.power(B, 30)
    G = np.power(G, 20)
    R = np.power(R, 20)
    B = B*255
    G = G*255
    R = R*255

    # B = B.round().astype(np.uint8)
    # B= cv2.medianBlur(B,15)
    B = cv2.blur(B, (25, 25))
    B = cv2.blur(B, (25, 25))
    B = cv2.blur(B, (25, 25))
    # B = cv2.blur(B, (5, 5))
    # B = cv2.blur(B, (5, 5))
    # B = cv2.blur(B, (5, 5))

    # G = G.round().astype(np.uint8)
    # G= cv2.medianBlur(G,15)
    G = cv2.blur(G, (25, 25))
    G = cv2.blur(G, (25, 25))
    G = cv2.blur(G, (5, 5))
    G = cv2.blur(G, (5, 5))
    G = cv2.blur(G, (5, 5))

    R= cv2.blur(R, (25, 25))
    R= cv2.blur(R, (25, 25))
    R= cv2.blur(R, (25, 25))

    # R_flatten = R.flatten()
    # for i in R_flatten:
    #     if i!=0:
    #         i +=100
    # R = R_flatten.reshape(R.shape)
    # plotRGB(R,G,B)
    Y = (G+3*B)/4  # B��Gͨ���ϳ�

    # R = np.floor(R).round().astype(np.uint8)
    # cv2.imshow('CHANNEL_R',R)
    # cv2.waitKey(0)
    G = np.floor(G).round().astype(np.uint8)
    B = np.floor(B).round().astype(np.uint8)


    Y = np.floor(Y).round().astype(np.uint8)
    # plt.figure(figsize=(10,10))
    # plt.imshow(Y,cmap='gray')
    ret, imgthresh = cv2.threshold(Y, 0, 255,
                                cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)  # Otsu��ֵ����,ת��Ϊ��ֵͼ

    kernel = np.ones((3, 3), np.uint8)  # ������̬�任�����

    imgopen = cv2.morphologyEx(imgthresh, cv2.MORPH_OPEN,
                            kernel, iterations=3)  # ��̬�任��������

    imgbg = cv2.dilate(imgopen, kernel, iterations=5)  # ���Ͳ�����ȷ������

    imgdist = cv2.distanceTransform(imgopen, cv2.DIST_L2, 0)  # ����ת������ȥȷ��ǰ��

    ret, imgfg = cv2.threshold(imgdist,
                            0.7*imgdist.max(), 255, 2)  # �Ծ���ת�����������ֵ����

    imgfg = np.uint8(imgfg)  # ת��Ϊ���������ǰ��

    ret, markers = cv2.connectedComponents(imgfg)  # �����ֵ������

    unknown = cv2.subtract(imgbg, imgfg)  # ȷ��λ��δ֪����

    markers = markers + 1  # ��1ʹ������Ϊ0

    markers[unknown == 255] = 0  # ��δ֪��������Ϊ0

    imgwater = cv2.watershed(img, markers)  # ִ�з�ˮ���㷨�ָ�ͼ��


    img[imgwater == -1] = [0, 255, 0]  # ��ԭͼ�б���ǵ�����Ϊ��ɫ

    return img