#
#   MAD MUSIC PLAYER WITH GESTURE
#

import os
import pygame
import tkinter as tk
from tkinter.filedialog import *
from tkinter import *
from mutagen.id3 import ID3,TIT2
from mutagen.easyid3 import EasyID3
import mutagen
from PIL import Image,ImageTk
import os
import pygame
import tkinter as tk
from tkinter.filedialog import *
from tkinter import *
from mutagen.id3 import ID3,TIT2
from mutagen.easyid3 import EasyID3
import mutagen
from PIL import Image,ImageTk
import cv2
import imutils
import numpy as np
import math
import time

global bg
bg = None
global cnts

def run_avg(image, aWeight):
    global bg
    # initialize the background
    if bg is None:
        bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, bg, aWeight)

def segment(image, threshold=25):
    global bg
    # find the absolute difference between background and current frame
    diff = cv2.absdiff(bg.astype("uint8"), image)

    # threshold the diff image so that we get the foreground
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # get the contours in the thresholded image
    cnts, hierarchy = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)

def atul(event):
    # initialize weight for running average
    aWeight = 0.5
    
    # get the reference to the webcam
    camera = cv2.VideoCapture(0)

    # region of interest (ROI) coordinates
    top, right, bottom, left = 10, 350, 225, 590

    # initialize num of frames
    num_frames = 0

    # keep looping, until interrupted
    while(True):
        # get the current frame
        (grabbed, frame) = camera.read()

        # resize the frame
        frame = imutils.resize(frame, width=700)

        # flip the frame so that it is not the mirror view
        frame = cv2.flip(frame, 1)

        # clone the frame
        clone = frame.copy()

        # get the height and width of the frame
        (height, width) = frame.shape[:2]

        # get the ROI
        roi = frame[top:bottom, right:left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # to get the background, keep looking till a threshold is reached
        # so that our running average model gets calibrated
        if num_frames < 30:
            run_avg(gray, aWeight)
        else:
            # segment the hand region
            hand = segment(gray)

            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented) = hand

                # draw the segmented region and display the frame
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                #cv2.imshow("Thesholded", thresholded)
                contours,hierarchy = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contour = max(contours, key=lambda x: cv2.contourArea(x))
                hull = cv2.convexHull(contour)
                hull = cv2.convexHull(contour, returnPoints=False)
                defects = cv2.convexityDefects(contour, hull)
                count_defects = 0


                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(contour[s][0])
                    end = tuple(contour[e][0])
                    far = tuple(contour[f][0])

                    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

                    # if angle > 90 draw a circle at the far point
                    if angle <= 90:
                        count_defects += 1
                        cv2.circle(clone, far, 1, [0, 0, 255], -1)

                    cv2.line(clone, start, end, [0, 255, 0], 2)

                # Print number of fingers
                #if count_defects == 0:
                    #print("next")
                    #time.sleep(3)

                if count_defects == 1:
                    play_song('event')
                  #  print("prev")
                   # time.sleep(3)

                elif count_defects == 2:
                    next_song('event')
                    print("next")
                    time.sleep(3)

                elif count_defects == 3:
                    previous_song('previous')
                    time.sleep(3)
                elif count_defects == 4:
                    pause_song('pause')
                    time.sleep(3)

                else:
                    pass



        # draw the segmented hand
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        # increment the number of frames
        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)

        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break

    # free up memory
    camera.release()
    cv2.destroyAllWindows()

page=tk.Tk()
page.title("MAD Music PLAYER")
page.minsize(width= 680, height= 480)
page.maxsize(width= 680, height= 480)

page.iconbitmap(r'C:\\Users\\DEV\\favicon.ico')

listofsongs=[]
index=0
realname=[]
count=0

v=StringVar()
songlabel=tk.Label(page,textvariable=v,font=("bold",15),bg="blue",fg="white")
songlabel.pack(fill=X)

#                  Functions 

def next_song(event):
    global index
    global listofsongs
    index+=1
    if(index >= len(listofsongs)):
        index=0
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def previous_song(event):
    global index
    global listofsongs
    index-=1
    if(index<=-1):
        index=len(listofsongs)-1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def pause_song(event):
    pygame.mixer.music.pause()

def play_song(event):
    pygame.mixer.music.unpause()
    
def stop_song(event):
    pygame.mixer.music.stop()

def directorychooser():
    directory=askdirectory()
    os.chdir(directory)
    global count
    for files in os.listdir(directory):
        if(files.endswith(".mp3")):
            realdir=os.path.realpath(files)
            count+=1
            meta = mutagen.File(realdir, easy=True)
            #audio=EasyID3(realdir)
            #print(audio[TIT2].text[0])
            realname.append(TIT2(text=files))
            listofsongs.append(files)
    global index
    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    pygame.mixer.music.play()
    v.set(realname[index])
directorychooser()

def get_volume():
    ps1=Label(page,text="SET VOLUME",font=20,bg="blue",fg="white")
    ps1.pack(side=BOTTOM)
    global pss
    pss=tk.Entry(page)
    pss.pack(side=BOTTOM)
    v1=tk.Button(page,command=set_volume,text="Enter",bg="blue",fg="white")
    v1.pack(side=BOTTOM)
    
def set_volume():
    volume=float(pss.get())
    pygame.mixer.music.set_volume(volume)
    
def countsong():
    ul2=tk.Label(page,text="Jump to specific song",fg="white",bg='black')
    ul2.pack(side=BOTTOM)
    global u2
    u2=tk.Entry(page)
    u2.pack(side=BOTTOM)
    goto=tk.Button(page,command=set_count,text="GO TO",bg="indigo",fg='white')
    goto.pack(side=BOTTOM)

    
def set_count():
    global index
    global count
    global listofsongs
    a=int(u2.get())
    if(count>=a):
        index=a-1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()
    
def instruction():
    inst=tk.Tk()
    l1=tk.Label(inst,text="# In Left side of screen is showing the list of songs\n # Below the menu_bar it displaying the name of the song which is currently playing\n # PLAY is used to play the music\n # PAUSE is for pause the music\n # NEXT is use to play next song in the list,if last is playing then it will play first song in the list\n # PREV is use to play the prev song in the list, if first is playing then it will play last song in the list\n # STOP is use for stop the music and play when you click NEXT or PREV\n # REPLAY is for replay that particular music\n # SET VOLUME is use to set the volume and the range between 0.0 and 1.0 after the press the Enter to change\n # Jump to specific song it allows us to jump the specific song according to entered value and if range is not match then it\n   will play the same song which is playing\n\n# For enabling a gesture part you have to click on EN gesture and to disable you have to cick q on keyboard\n   show fingure 1 for play the music\n   show fingure 2 for next song\n   show 3 fingures for previous song\n   show 4 fingures for pause\n\nNOTE\n1: You need to hold your fingure for 3-4 second\n2: The part of gesture is under consturction\n3: If you use gestures every buttons will stop working",bg="red",fg="white",bd=50)
    #button=tk.Label(page,text="mad mad")
    l1.pack(side="top")
    inst.mainloop()

def about():
    about=tk.Tk()
    l2=tk.Label(about,text="# MAD GROUP OF ASSOCIATION is create by three members of college which made his first project in college after a 15 days of python internship in IES College Of Technology,Bhopal \n # MAD is a actually an acronym of 3 memeber i.e Massom,Atul,Dev which are working together to make this project a huge success\n\n # First member of the group i.e Massom Khan work on basic GUI/front-end\n # Second member of a group is Atul Singh work on Gesture Part\n # Third memeber of a group is Dev Maheshwari which is work on back-end\n\n# After a lot of experiment and research and under a guidence of a trainer we develop a music player in 5 days\n# So we will hope you will enjoy",bg="red",fg="white",bd=50)
    l2.pack()
    about.mainloop()
    
def updatelabel():
    global index
    global songname
    v.set(realname[index])
    #return songname

def replay_song(event):
    pygame.mixer.music.rewind()

#       Creating a list box for display the songs

listbox=Listbox(page,bg="black",fg="white",width="20",height="80")
label=Label(page,text='MAD\n Music\n Player',font=("bold",40),bg="black",fg="white")
label.pack(side=LEFT,fill=Y)
listbox.pack(side=RIGHT)

realname.reverse()


for i in realname:
    listbox.insert(0,i)
realname.reverse()

Photo=tk.PhotoImage(file='C:\\Users\\DEV\\p.png',master=page)
canvas = tk.Canvas(master=page, width=250,height=230,bg="black")
canvas.create_image(0,0, anchor='nw', image=Photo)
canvas.place(x=226,y=38)
#canvas.pack(side=TOP)

#   Creating a menus

menu1=Menu(page)
page.config(menu=menu1)
submenu=Menu(menu1,tearoff=0)
menu1.add_cascade(label="file",menu=submenu)
submenu.add_command(label="INSTRUCTION",command=instruction) 
submenu.add_command(label="PLAY",command=play_song) 
submenu2=Menu(menu1,tearoff=0)
menu1.add_cascade(label="ABOUT",menu=submenu2)
submenu2.add_command(label="About Us",command=about) 

#Creating a Buttons

previousbutton=tk.Button(page,text="PREV",font=50,fg="white",bg="blue")
previousbutton.place(x=169,y=72)
#previousbutton.pack() 

#instruction_button=tk.Button(page,text="")

playbutton=tk.Button(page,text=" PLAY ",font=20,fg="black",bg="white")
playbutton.place(x=169,y=40)
#playbutton.pack()

EN=tk.Button(page,text="EN gesture",font=20,fg="white",bg="black")
EN.pack(side=BOTTOM)

#DIS=tk.Button(page,text=" DIS gesture ",font=20,fg="black",bg="white")
#DIS.pack(side=BOTTOM)

pausebutton=tk.Button(page,text="PAUSE ",font=20,fg="black",bg="white")
pausebutton.place(x=480,y=40)
#pausebutton.pack() 
   
nextbutton=tk.Button(page,text="NEXT",font=20,fg="white",bg="blue")
nextbutton.place(x=480,y=72)
#nextbutton.pack()        

stopbutton=tk.Button(page,text="STOP",font=20,fg="black",bg="white")
stopbutton.place(x=169,y=104)
#stopbutton.pack()

ps2=tk.Button(page,text="REPLAY",font=20,fg="black",bg="white")
ps2.place(x=480,y=104)
#ps2.pack()

#Linking a Buttons to Function

nextbutton.bind('<Button-1>',next_song)
previousbutton.bind('<Button-1>',previous_song)
pausebutton.bind('<Button-1>',pause_song)
playbutton.bind('<Button-1>',play_song)
stopbutton.bind('<Button-1>',stop_song)
ps2.bind('<Button-1>',replay_song)
EN.bind('<Button-1>',atul)
get_volume()
countsong()


    
songlabel.pack()  

page.mainloop() #Closing a window
pygame.mixer.music.stop()  #After closing a window the music will automatic stop