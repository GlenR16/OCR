from lib2to3.pgen2.token import LEFTSHIFT
from datetime import datetime
from textwrap import fill, wrap
import tkinter as tk
from tkinter import ANCHOR, font
from tkinter import filedialog
import pytesseract
import easyocr
import tkinter.ttk as ttk
import os
import subprocess
import PyPDF2
from PIL import ImageGrab,Image
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
    Y,
    TOP
)
import ctypes
#                     Change this >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

ctypes.windll.shcore.SetProcessDpiAwareness(1)
class App(tk.Tk):
    
    # App Constructor
    def __init__(self):
        super().__init__()
        self.title("OCR App")
        self.geometry("1920x1080")
        #self.resizable(False, False)
        self.dark = '#333'
        self.white = '#ffffff'
        self.iconbitmap("./Images/icon.ico")
        self.tk.call("source", "sun-valley.tcl")
        self.back_img = tk.PhotoImage(file=f"./Images/back.png")
        self.draw_img = tk.PhotoImage(file=f"./Images/draw.png")
        self.upload_img = tk.PhotoImage(file=f"./Images/image.png")
        self.upload_pdf = tk.PhotoImage(file=f"./Images/pdf.png")
        self.camera = tk.PhotoImage(file=f"./Images/camera.png")
        self.reset_img = tk.PhotoImage(file=f"./Images/reset.png")
        self.scan_img = tk.PhotoImage(file=f"./Images/scan.png")
        self.current_drawing = tk.StringVar()
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
        self.image_button.pack_forget()
        # Show the draw screen and create canvas
        self.options_frame = tk.LabelFrame(self,bg=self.dark,text="Menu",font=("Courier",18),fg=self.white)
        self.options_frame.pack(side=LEFT,anchor='nw',padx=10,pady=10)
        #Buttons of the side options
        self.back_button = tk.Button(self.options_frame,image=self.back_img,borderwidth=0,highlightthickness=5,command=self.backCallBack)
        self.back_button.pack(padx=20,pady=20)
        self.reset_button = tk.Button(self.options_frame,image=self.reset_img,borderwidth=0,highlightthickness=5,command=self.resetDrawPane)
        self.reset_button.pack(padx=20,pady=20)
        self.scan_button = tk.Button(self.options_frame,image=self.scan_img,borderwidth=0,highlightthickness=5,command=self.save_img)
        self.scan_button.pack(padx=20,pady=20)
        #Frame and canvas to draw
        self.paint_frame = tk.LabelFrame(self,bg=self.dark,text="Paint",font=("Courier",18),fg=self.white)
        self.paint_frame.pack(padx=0,pady=0)
        self.painter=tk.Canvas(self.paint_frame, bg='white',height=self.winfo_screenheight()-250,width=self.winfo_screenwidth()-400)
        self.painter.bind('<B1-Motion>', self.paint)
        self.painter.pack(padx=10,pady=10)



    def resetDrawPane(self):
        self.painter.delete('all')


    def backCallBack(self):
        try:
            self.options_frame.pack_forget()
            self.back_button.pack_forget()
            self.painter.pack_forget()
            self.paint_frame.pack_forget()
        except:
            pass
        try:
            self.back_button1.pack_forget()
            self.text.pack_forget()
        except:
            pass
        self.title_frame.pack(padx=10,pady=10)
        self.heading.pack(pady=25)
        self.main_frame.pack()
        self.left_frame.pack(side=LEFT)
        self.right_frame.pack(side=RIGHT)
        self.camera_button.pack(padx=20,side=tk.LEFT)
        self.draw_button.pack(padx=20,side=tk.LEFT)
        self.pdf_button.pack(padx=20,side=tk.LEFT)
        self.image_button.pack(padx=20,side=tk.LEFT)
        
    def save_img(self):
        x=self.painter.winfo_rootx()+self.painter.winfo_x()
        y=self.painter.winfo_rooty()+self.painter.winfo_y()-50
        x1=x+self.painter.winfo_width()-10
        y1=y+self.painter.winfo_height()
        now = "./drawings/"+str(datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p"))+".jpg"
        ImageGrab.grab().crop((x,y,x1,y1)).save(now)
        #convert image to text from path
        try:
            ans = pytesseract.image_to_string(Image.open(now))
            print(ans)
            self.options_frame.pack_forget()
            self.back_button.pack_forget()
            self.painter.pack_forget()
            self.paint_frame.pack_forget()
            self.back_button1 = tk.Button(self,image=self.back_img,borderwidth=0,highlightthickness=5,command=self.backCallBack)
            self.back_button1.pack(padx=20,pady=20)
            self.text = tk.Text(self, wrap=WORD, bd=0, height=self.winfo_height()-500, width=self.winfo_width()-100)
            self.text.insert(END, ans)
            self.text.pack()
        except:
            self.text = tk.Label(self,text="No file Selected",font=("Amaranth",25),bg=self.dark,fg=self.white)
            self.text.pack(padx=10,pady=10)
        

    def paint(self,event):
        # get x1, y1, x2, y2 co-ordinates
        x1, y1 = (event.x-3), (event.y-3)
        x2, y2 = (event.x+3), (event.y+3)
        color = "black"
        # display the mouse movement inside canvas
        self.painter.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def uploadCallBack(self,pdf=False):
        # Hide previous things
        self.main_frame.pack_forget()
        self.title_frame.pack_forget()
        self.right_frame.pack_forget()
        self.left_frame.pack_forget()
        self.draw_button.pack_forget()
        self.image_button.pack_forget()
        self.camera_button.pack_forget()
        self.pdf_button.pack_forget()
        self.back_button1 = tk.Button(self,image=self.back_img,borderwidth=0,highlightthickness=5,command=self.backCallBack)
        self.back_button1.pack(padx=20,pady=20)
        # Show the upload screen.
        if pdf==False:
            uploaded = filedialog.askopenfilename(filetypes=(("JPG files","*.jpeg"),("PNG files","*.png")))
            try:
                ans = pytesseract.image_to_string(Image.open(uploaded))
                self.text = tk.Text(self, wrap=WORD, bd=0, height=self.winfo_height()-500, width=self.winfo_width()-100)
                self.text.insert(END, ans)
                self.text.pack()
            except:
                self.text = tk.Label(self,text="No file Selected",font=("Amaranth",25),bg=self.dark,fg=self.white)
                self.text.pack(padx=10,pady=10)
        else:
            uploaded = filedialog.askopenfilename(filetypes=(("PDF files","*.pdf"),))
            try:
                pdfFile = open(uploaded, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFile) 
                ans = ""
                for i in range(pdfReader.numPages):
                    pageObj = pdfReader.getPage(i) 
                    ans += pageObj.extractText()
                self.text = tk.Text(self, wrap=WORD, bd=0, height=self.winfo_height()-500, width=self.winfo_width()-100)
                self.text.insert(END, ans)
                self.text.pack()
            except:
                self.text = tk.Label(self,text="No file Selected",font=("Amaranth",25),bg=self.dark,fg=self.white)
                self.text.pack(padx=10,pady=10)
                
            



    # Main Screen
    def main(self):
        self.title_frame = tk.Frame(self,bg=self.dark)
        self.heading = tk.Label(self.title_frame,text="OCR App",font=("Amaranth",44),bg=self.dark,fg=self.white)
        self.heading.pack(pady=25)
        self.title_frame.pack(padx=10,pady=10)
        self.main_frame = tk.Frame(self,bg=self.dark)
        self.left_frame = tk.Frame(self,bg=self.dark)
        self.right_frame = tk.Frame(self,bg=self.dark)
        self.draw_button = tk.Button(self.left_frame,image=self.draw_img,border='0',borderwidth=0,highlightthickness=5,command=self.drawCallBack)
        self.image_button = tk.Button(self.right_frame,image=self.upload_img,border='0',borderwidth=0,highlightthickness=5,command=lambda: self.uploadCallBack())
        self.pdf_button = tk.Button(self.right_frame,image=self.upload_pdf,border='0',borderwidth=0,highlightthickness=5,command=lambda: self.uploadCallBack(True))
        self.camera_button = tk.Button(self.left_frame,image=self.camera,border='0',borderwidth=0,highlightthickness=5,command=None)
        self.main_frame.pack()
        self.left_frame.pack(side=LEFT)
        self.right_frame.pack(side=RIGHT)
        self.camera_button.pack(padx=20,side=tk.LEFT)
        self.draw_button.pack(padx=20,side=tk.LEFT)
        self.pdf_button.pack(padx=20,side=tk.LEFT)
        self.image_button.pack(padx=20,side=tk.LEFT)



if __name__ == "__main__":
    app = App()
    app.mainloop()
