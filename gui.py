from tkinter import *
from datetime import datetime
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
        self.time_label = Label(self,text="10:40:30",bg="#353231",fg="#EEE110")
        #self.time_label.place(x=50,y=150)
        #self.time_label.place(x=10,y=10)
        self.time_label.place(x=math.floor(width*0.55), y=math.floor(height*0.01))
        self.time_now()
    def time_now(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.time_label.after(1000,self.time_now)
root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f'{width}x{height}')
#root.configure(bg="#353231")
app = Window(root)
root.mainloop()
