from tkinter import *
from tkinter import Toplevel

root = Tk()

def click_open_window():
    global top,vertical,horizontal
    
    top = Toplevel()
    top.geometry("500x500")
    
    vertical = Scale(top,from_=50,to=800)
    horizontal = Scale(top,from_=50,to=800,orient=HORIZONTAL)
    vertical.pack(side = "right")
    horizontal.pack(side='bottom')
    
    btn_adjust['state']="normal"

def adjust():
    global horizontal,vertical
    top.geometry(str(horizontal.get())+"x"+str(vertical.get()))
    
btn_new = Button(root,text="Click to open new window",command=click_open_window).pack(padx=20,pady=20)
btn_adjust = Button(root,text='Adjust window',command=adjust,state=DISABLED)

btn_adjust.pack(padx=10,pady=20)    
root.mainloop()