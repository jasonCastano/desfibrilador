#!/usr/bin/env python3
from tkinter import *
from tkinter.font import BOLD, Font
from datetime import datetime
from datetime import date

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import math
import rospy
from std_msgs.msg import Int16, String
from threading import Thread
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight() 
    def init_window(self):
        self.master.title("Desfibrilador")
        self.pack(fill=BOTH,expand=True)
        self.configure(bg="#353231")
        self.time_label = Label(self,bg="#353231",fg="#EEE110")
        self.time_label.place(x=math.floor(width*0.55), y=math.floor(height*0.01))
        self.time_now()
        self.date_label = Label(self,bg="#353231",fg="#EEE110")
        self.date_label.place(x=math.floor(width*0.7), y=math.floor(height*0.01))
        self.date_now()
        data_frame_height = math.floor(height*0.25)
        data_frame = Frame(self, bg = "#A8A5A4", width=width, height=data_frame_height)
        data_frame.place(x=0,y=math.floor(height*0.09))
        data_small_label_font = Font(self.master, size=10, weight=BOLD)

        fc_label = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="FC", font=data_small_label_font)
        fc_label.place(x=math.floor(width*0.05),y=math.floor(data_frame_height*0.01))
        
        data_big_label_font = Font(self.master, size=40, weight=BOLD)
        self.lpm_value = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="0", font=data_big_label_font)
        self.lpm_value.place(x=math.floor(width*0.05),y=math.floor(data_frame_height*0.2))
        
        lpm_label = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="lpm", font=data_small_label_font)
        lpm_label.place(x=math.floor(width*0.05),y=math.floor(data_frame_height*0.8))
        
        modo_label = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="MODO", font=data_small_label_font)
        modo_label.place(x=math.floor(width*0.25),y=math.floor(data_frame_height*0.01))
        self.modo_value = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="", font=data_big_label_font)
        self.modo_value.place(x=math.floor(width*0.25),y=math.floor(data_frame_height*0.2))
        
        carga_label = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="CARGA", font=data_small_label_font)
        carga_label.place(x=math.floor(width*0.45),y=math.floor(data_frame_height*0.01))
        carga_frame = Frame(data_frame, bg = "#827F7D", width=math.floor(width*0.25), height=math.floor(data_frame_height*0.6))
        carga_frame.place(x=math.floor(width*0.38),y=math.floor(data_frame_height*0.2))
        self.carga_value = Label(carga_frame, bg="#827F7D",fg="#34EB13", text="0", font=data_big_label_font)
        self.carga_value.place(x=math.floor(width*0.15*0.22),y=math.floor(data_frame_height*0.25*0.01))
        
        sinc_label = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="SINC", font=data_small_label_font)
        sinc_label.place(x=math.floor(width*0.71),y=math.floor(data_frame_height*0.01))
        sinc_frame = Frame(data_frame, bg = "#827F7D", width=math.floor(width*0.12), height=math.floor(data_frame_height*0.6))
        sinc_frame.place(x=math.floor(width*0.68),y=math.floor(data_frame_height*0.2))
        self.sinc_value = Label(sinc_frame, bg="#827F7D",fg="#34EB13", text="", font=data_big_label_font)
        self.sinc_value.place(x=math.floor(width*0.12*0.22),y=math.floor(data_frame_height*0.25*0.01))

        descargas_label = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="DESCARGAS", font=data_small_label_font)
        descargas_label.place(x=math.floor(width*0.81),y=math.floor(data_frame_height*0.01))
        descargas_frame = Frame(data_frame, bg = "#827F7D", width=math.floor(width*0.12), height=math.floor(data_frame_height*0.6))
        descargas_frame.place(x=math.floor(width*0.82),y=math.floor(data_frame_height*0.2))
        self.descargas_value = Label(descargas_frame, bg="#827F7D",fg="#34EB13", text="0", font=data_big_label_font)
        self.descargas_value.place(x=math.floor(width*0.12*0.22),y=math.floor(data_frame_height*0.25*0.01))
        
        ecg_label = Label(self, bg="#353231",fg="#34EB13", text="ECG", font=data_small_label_font)
        ecg_label.place(x=math.floor(width*0.01),y=math.floor(height*0.35))
        
        self.fig, self.ax = plt.subplots(facecolor="#353231")
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_facecolor("#353231")
        global t
        global ecg_data
        self.line, = self.ax.plot(t, ecg_data, color="#34EB13", linestyle="solid", linewidth=3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().config(width=width, height=math.floor(height*0.25))
        self.canvas.get_tk_widget().place(x=math.floor(width*0.01),y=math.floor(height*0.38))
        
        self.atencion_label = Label(self, bg="#353231",fg="#E30E0E", text="", font=data_small_label_font)
        self.atencion_label.place(x=math.floor(width*0.01),y=math.floor(height*0.7))

    def time_now(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.time_label.after(1000,self.time_now)
    def date_now(self):
        now = date.today()
        current_date = now.strftime("%b-%d-%Y")
        self.date_label.config(text=current_date)
        self.date_label.after(3600000,self.date_now)

def lpm_data(data):
    global app
    app.lpm_value.config(text=str(data.data))

def modo_data(data):
    global app
    m = data.data
    app.modo_value.config(text=m)
    if m == "M":
        app.atencion_label.config(text="")
    elif m == "D":
        app.atencion_label.config(text="ATENCIÓN ANTE UNA ARRITMIA DE CARÁCTER VENTRICULAR")
    elif m == "S":
        app.atencion_label.config(text="ATENCIÓN ANTE UNA ARRITMIA AURICULAR")
def carga_data(data):
    global app
    app.carga_value.config(text=data.data)
def sinc_data(data):
    global app
    app.sinc_value.config(text=data.data)
def descargas_data(data):
    global app
    app.descargas_value.config(text=str(data.data))

def animate(t,ecg_data,line):
    #global app
    #global ecg_data
    #global t
    #app.line.set_ydata(ecg_data)
    #app.line.set_xdata(t)
    
    line.set_data(t,ecg_data)

    #return app.line,

def ecg_plot(data):
    #global ani
    global app
    global ecg_data
    #print(data.data)
    ecg_data = np.delete(ecg_data,0)
    ecg_data = np.append(ecg_data,data.data)
    #app.ax.clear()
    #app.line = app.ax.plot(t, ecg_data, color="#34EB13", linestyle="solid", linewidth=3)
    
    ani = animation.FuncAnimation(app.fig, animate, fargs=(t,ecg_dat,app.line),interval=100, blit=False)
    #app.ax.set_xticks([])                                                  
    #app.ax.set_yticks([]) 
    app.canvas.draw()

t = np.arange(0,5,0.004)
ecg_data = np.zeros((1250))
#ecg_data = np.sin(t)
root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f'{width}x{height}')
app = Window(root)
#ROS
rospy.init_node("gui_node", anonymous=False)
rospy.Subscriber("/desfibrilador/lpm", Int16, lpm_data)
rospy.Subscriber("/desfibrilador/modo",String,modo_data)
rospy.Subscriber("/desfibrilador/carga",String,carga_data)
rospy.Subscriber("/desfibrilador/sinc",String,sinc_data)
rospy.Subscriber("/desfibrilador/descargas",Int16,descargas_data)
rospy.Subscriber("/desfibrilador/ecg_signal",Int16,ecg_plot)
root.mainloop()
