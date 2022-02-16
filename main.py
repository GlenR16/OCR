from lib2to3.pgen2.token import LEFTSHIFT
import tkinter as tk
from tkinter import ANCHOR, font
from tkinter import filedialog
import tkinter.ttk as ttk
import os
import subprocess
from tkinter.constants import (
    BOTTOM,
    HORIZONTAL,
    LEFT,
    NSEW,
    TRUE,
    WORD,
    END,
    RIGHT,
    BOTH,
    X,
    TOP
)
import ctypes
from attr import field

ctypes.windll.shcore.SetProcessDpiAwareness(1)
class App(tk.Tk):
    
    # App Constructor
    def __init__(self):
        super().__init__()
        self.title("OCR App")
        self.geometry("900x800")
        self.resizable(False, False)
        self.dark = '#333'
        self.white = '#ffffff'
        self.iconbitmap("./Images/icon.ico")
        self.tk.call("source", "sun-valley.tcl")
        self.back_img = tk.PhotoImage(file=f"./Images/back.png")
        self.draw_img = tk.PhotoImage(file=f"./Images/draw.png")
        self.upload_img = tk.PhotoImage(file=f"./Images/upload.png")
        self.reset_img = tk.PhotoImage(file=f"./Images/reset.png")
        self.configure(background=self.dark)
        self.main()
    
    # Click on the draw button calls here.
    def drawCallBack(self):
        # Hide previous things
        self.title_frame.pack_forget()
        self.heading.pack_forget()
        self.left_frame.pack_forget()
        self.right_frame.pack_forget()
        self.main_frame.pack_forget()
        self.draw_button.pack_forget()
        self.upload_button.pack_forget()
        # Show the draw screen and create canvas
        self.options_frame = tk.LabelFrame(self,bg=self.dark,text="Menu",font=("Courier",18),fg=self.white)
        self.options_frame.pack(side=LEFT,anchor='nw',padx=10,pady=10)
        #Buttons
        self.back_button = tk.Button(self.options_frame,image=self.back_img,borderwidth=0,highlightthickness=5,command=self.backCallBack)
        self.back_button.pack(padx=20,pady=20)
        self.reset_button = tk.Button(self.options_frame,image=self.reset_img,borderwidth=0,highlightthickness=5,command=self.resetDrawPane)
        self.reset_button.pack(padx=20,pady=20)
        #Frame and canvas to draw
        self.paint_frame = tk.LabelFrame(self,bg=self.dark,text="Paint",font=("Courier",18),fg=self.white)
        self.paint_frame.pack(padx=10,pady=10)
        self.painter=tk.Canvas(self.paint_frame, bg='white',height=700,width=600)
        self.painter.bind('<B1-Motion>', self.paint)
        self.painter.pack(padx=10,pady=10)



    def resetDrawPane(self):
        self.painter.delete('all')

    


    def backCallBack(self):
        if self.options_frame.winfo_ismapped():
            self.options_frame.pack_forget()
            self.back_button.pack_forget()
            self.painter.pack_forget()
            self.paint_frame.pack_forget()
        else:
            pass
        self.heading.pack(pady=25)
        self.title_frame.pack(padx=10,pady=10)
        self.main_frame.pack()
        self.left_frame.pack(side=LEFT)
        self.right_frame.pack(side=RIGHT)
        self.draw_button.pack(padx=20)
        self.upload_button.pack(padx=20)
        

    def paint(self,event):
        # get x1, y1, x2, y2 co-ordinates
        x1, y1 = (event.x-3), (event.y-3)
        x2, y2 = (event.x+3), (event.y+3)
        color = "black"
        # display the mouse movement inside canvas
        self.painter.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def uploadCallBack(self):
        # Hide previous things
        self.title_frame.pack_forget()
        self.draw_button.pack_forget()
        self.upload_button.pack_forget()
        # Show the upload screen.
        self.uploaded = filedialog.askopenfile(filetypes=(("jpg files","*.jpeg"),("png files","*.png")))
        self.imageshow = tk.Canvas(self,height=700,width=600)
        self.imageshow.pack()
        self.imageshow.create_image(20,20,anchor='nw',image=tk.PhotoImage(data=self.uploaded))


    # Main Screen
    def main(self):
        self.title_frame = tk.Frame(self,bg=self.dark)
        self.heading = tk.Label(self.title_frame,text="OCR App",font=("Courier",44),bg=self.dark,fg=self.white)
        self.heading.pack(pady=25)
        self.title_frame.pack(padx=10,pady=10)
        self.main_frame = tk.Frame(self,bg=self.dark)
        self.left_frame = tk.Frame(self,bg=self.dark)
        self.right_frame = tk.Frame(self,bg=self.dark)
        self.draw_button = tk.Button(self.left_frame,image=self.draw_img,border='0',borderwidth=0,highlightthickness=5,command=self.drawCallBack)
        self.upload_button = tk.Button(self.right_frame,image=self.upload_img,border='0',borderwidth=0,highlightthickness=5,command=self.uploadCallBack)
        self.main_frame.pack()
        self.left_frame.pack(side=LEFT)
        self.right_frame.pack(side=RIGHT)
        self.draw_button.pack(padx=20)
        self.upload_button.pack(padx=20)



if __name__ == "__main__":
    app = App()
    app.mainloop()
