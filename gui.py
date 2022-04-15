from tkinter import *
from tkinter.font import BOLD, Font
from datetime import datetime
from datetime import date
import math
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
        fc_label.place(x=width*0.05,y=data_frame_height*0.01)
        data_big_label_font = Font(self.master, size=40, weight=BOLD)
        self.lpm_value_label = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="80", font=data_big_label_font)
        self.lpm_value_label.place(x=width*0.05,y=data_frame_height*0.2)
        lpm_label = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="lpm", font=data_small_label_font)
        lpm_label.place(x=width*0.05,y=data_frame_height*0.8)
        modo_label = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="MODO", font=data_small_label_font)
        modo_label.place(x=width*0.25,y=data_frame_height*0.01)
        self.modo_value_label = Label(data_frame, bg="#A8A5A4",fg="#34EB13", text="M", font=data_big_label_font)
        self.modo_value_label.place(x=width*0.25,y=data_frame_height*0.2)
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
root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f'{width}x{height}')
app = Window(root)
root.mainloop()
