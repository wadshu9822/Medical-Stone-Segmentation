from doctest import master
import os
from pickletools import string1
from typing import Tuple
import cv2
import torch
import screeninfo
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Button, filedialog
import tkinter.font as tkFont
from frameseg import frame_seg
# from Detection.Utils import ResizePadding
from CameraLoader import CamLoader, CamLoader_Q
# from DetectorLoader import TinyYOLOv3_onecls

# from PoseEstimateLoader import SPPE_FastPose
# from fn import draw_single

# from Track.Tracker import Detection, Tracker
# from ActionsEstLoader import TSSTG





def get_monitor_from_coord(x, y):  # multiple monitor dealing.
    monitors = screeninfo.get_monitors()
    for m in reversed(monitors):
        if m.x <= x <= m.width + m.x and m.y <= y <= m.height + m.y:
            return m
    return monitors[0]

class main:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title('Medical Stone Segmentation')
        self.master.protocol('WM_DELETE_WINDOW', self._on_closing)
        self.main_screen = get_monitor_from_coord(master.winfo_x(), master.winfo_y())

        # self.width = int(self.main_screen.width * .5)
        # self.height = int(self.main_screen.height * .6)
        self.width =1200
        self.height =900
        self.xcoordinate = []
        self.ycoordinate = []

        self.master.geometry('{}x{}'.format(self.width, self.height))
        
        self.cam = None # 用于调用相机的参数
        # 在tk.TK()上创建画布
        self.canvas = tk.Canvas(master, width=self.width, height=self.height)
        self.seg = False
        self.canvas.pack()
        self.canvas.bind("<Button-3>", self.callback)

        # Load Models
        # self.resize_fn = ResizePadding(416, 416)
        # self.models = Models(device=device)

        self.select_cam()  # 先显示button和menu，此时进入一个循环，直到点击事件
        self.delay = 10
        self.load_cam(self.filepath)  # 若使用相机则清空画布，加载相机
        self.update()
            # print('helloA')


    def key(self,event):
        print("pressed", repr(event.char))


    def callback(self,event):
        self.xcoordinate.append(event.x)
        self.ycoordinate.append(event.y)
        print("clicked at", event.x, event.y)
        print(self.xcoordinate)


    def preproc(self, image):
        # image = self.resize_fn(image)
        # 图像预处理，转换为RGB通道
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    def startseg(self):
        self.seg = True
        self.delay = 1000  # 开始分割时，降低刷新速度


    def stopseg(self):
        self.seg = False
        self.xcoordinate = [] # 停止后清除坐标存储
        self.ycoordinate = []
        self.delay = 10


    def select_cam(self):
        menubar = tk.Menu(self.master)
        menubar.add_command(label='Load', command=self.get_filepath)
        menubar.add_command(label='Camera', command=self.use_camera)
        menubar.add_command(label='Exit', command=self.close_camera)
        self.master.config(menu=menubar)

        string1 = 'Medical Stone Segmentation'
        string2 = 'Click Load to process the video'
        self.text1 = self.canvas.create_text(int(self.width/2), int(self.height/3), anchor=tk.CENTER,\
            text=string1, font=tkFont.Font(family='Times', weight='bold', size=70), fill='red')
        self.text2 = self.canvas.create_text(int(self.width/2), int(self.height/2), anchor=tk.CENTER,\
            text=string2, font=tkFont.Font(family='Times', size=30))

        button1 = tk.Button(self.canvas, text='Load', command=self.get_filepath, anchor=tk.CENTER)
        button2 = tk.Button(self.canvas, text='Camera', command=self.use_camera, anchor=tk.CENTER)
        button3 = tk.Button(self.canvas, text='Exit', command=self.close_camera, anchor=tk.CENTER)
        button1.configure(width = 10, relief = tk.RAISED, fg='blue', font=tkFont.Font(family='Helvetica', size=25))
        button2.configure(width = 10, relief = tk.RAISED, fg='blue', font=tkFont.Font(family='Helvetica', size=25))
        button3.configure(width = 10, relief = tk.RAISED, fg='blue', font=tkFont.Font(family='Helvetica', size=25))
        self.bt1 = self.canvas.create_window(int(self.width/4), int(self.height*2/3), anchor=tk.CENTER, window=button1)
        self.bt2 = self.canvas.create_window(int(self.width/2), int(self.height*2/3), anchor=tk.CENTER, window=button2)
        self.bt3 = self.canvas.create_window(int(self.width*3/4), int(self.height*2/3), anchor=tk.CENTER, window=button3)
        button4 = tk.Button(self.canvas, text='Start', command=self.startseg, anchor=tk.CENTER)
        button4.configure(width = 10, relief = tk.RAISED, fg='blue', font=tkFont.Font(family='Helvetica', size=25))
        self.canvas.create_window(int(self.width*2/5), int(self.height*5/6), anchor=tk.CENTER, window=button4)
        button5 = tk.Button(self.canvas, text='Stop', command=self.stopseg, anchor=tk.CENTER)
        button5.configure(width = 10, relief = tk.RAISED, fg='blue', font=tkFont.Font(family='Helvetica', size=25))
        self.canvas.create_window(int(self.width*3/5), int(self.height*5/6), anchor=tk.CENTER, window=button5)
        self.master.mainloop()

    def get_filepath(self):
        self.filepath = filedialog.askopenfilename()
        self.seg = True
        # 选择要打开的文件，并返回文件名
        if self.filepath:
            self.canvas.delete(self.bt1,self.bt2,self.bt3,self.text1, self.text2)
            # 如果文件存在则删除原有的图片
            self.master.quit()
    
    def use_camera(self):
        self.filepath = 0  # 如果filepath为0，则代表可调用摄像头
        self.canvas.delete(self.bt1,self.bt2,self.bt3,self.text1, self.text2)
        self.master.quit()

    def close_camera(self):
        if self.cam:
            self.cam.stop()
            self.cam.__del__()
        self.master.destroy()

    def load_cam(self, source):
        if self.cam:  # 初始设定为None，即不会直接调用
            self.cam.__del__()

        if type(source) is str and os.path.isfile(source):  # 用于加载视频或者图片
            self.cam = CamLoader_Q(source, queue_size = 3000,preprocess=self.preproc).start()
            # 调用start()时就已经update 转换为RGB通道
        else:  # 加载摄像头
            self.cam = CamLoader(source,preprocess=self.preproc).start()

    def update(self):
        print(self.seg)
        if self.cam is None:
            return
        if self.cam.grabbed():
            frame = self.cam.getitem()
            frame = cv2.resize(frame, (800,600),
                               interpolation=cv2.INTER_CUBIC)
            # frame = self.models.process_frame(frame)
            if self.seg == True: #and len(self.xcoordinate) >= 2:
                frame = frame_seg(frame,self.xcoordinate,self.ycoordinate)
            # frame = cv2.resize(frame, (800,800),
                            #    interpolation=cv2.INTER_CUBIC)
            # frame = cv2.resize(frame, (self.canvas.winfo_width(), self.canvas.winfo_height()),
            #                    interpolation=cv2.INTER_CUBIC)
                              
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(600,400, image=self.photo, anchor=tk.CENTER)  # 坐标代表中心位置
            self.text2 = self.canvas.create_text(600,820, anchor=tk.CENTER,\
            text='click 2 points to start', font=tkFont.Font(family='Times', size=25, ),fill='red')
            print("hello")

        else:
            self.cam.stop()

        # if self.seg == False:
        self._cam = self.master.after(self.delay, self.update)
        # self.master.mainloop()
        # print(self.seg)


    
    def _on_closing(self):
        self.master.after_cancel(self._cam)
        if self.cam:
            self.cam.stop()
            self.cam.__del__()
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = main(root)
    root.mainloop()
