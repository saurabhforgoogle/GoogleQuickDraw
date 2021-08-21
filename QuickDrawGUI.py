import cv2
import os  
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
import random
import numpy as np
import tensorflow as tf  
model=tf.keras.models.load_model(r'C:\Users\saurabh\Documents\Desktop\Neural Network and Deep Learning\Google_Quickdraw\Quickdraw1.model')

Dirctr=r'C:\Users\saurabh\Documents\Desktop\Neural Network and Deep Learning\Google_Quickdraw\Data'
labels=[]
for file in os.listdir(Dirctr):
    labels.append([file[18:-4]])##remove earlier lines

def predict(img):

    import numpy as np
    img = np.array(img)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ##Remember always cv2 reads colors hence 255 is white and in matpolib its intensity actually!!!!!!
    img=cv2.resize(img,(28,28))

    for i in range(28):
        for j in range(28):
            img[i][j]=abs(img[i][j]-255.0)


    img=img/255.0
    img = img.reshape(1,28,28,1)
    #this return can be later used for more output access
    #it have labels added with corresponding vals and sorted with vals
    #print([labels[i]+[(model.predict([img])[0][i])] for i in range(len(labels))])
    return(sorted([labels[i]+[(model.predict([img])[0][i])] for i in range(len(labels))], key = lambda x: x[1] ,reverse=True))[0]
    
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        # Creating elements
        self.canvas = tk.Canvas(self, width=500, height=500, bg = "white", cursor="arrow")
        self.label = tk.Label(self, text="Thinking..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text = "Recognise", command =         self.classify_handwriting) 
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        #self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<ButtonRelease>", self.Classify_MouseRelease) #gives event to def Classify_MouseRelease (bind release key)
        self.canvas.bind("<B1-Motion>", self.draw_lines)
    def clear_all(self):
        self.canvas.delete("all")
    def Classify_MouseRelease(self,event):
        HWND = self.canvas.winfo_id() # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND) # get the coordinate of the canvas
        im = ImageGrab.grab(rect)
        digit = predict(im)
        self.label.configure(text= str(digit))
    def classify_handwriting(self):
        HWND = self.canvas.winfo_id() # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND) # get the coordinate of the canvas
        im = ImageGrab.grab(rect)
        digit = predict(im)
        self.label.configure(text= str(digit))
    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=10
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')
app = App()
mainloop()