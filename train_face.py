# Author : Uysal Altas
# Date   : 08/2018

import time
import numpy as np
import cv2
import os
import tkinter as tk
from PIL import Image, ImageTk

count = 0
cap = cv2.VideoCapture(0)
global button_path

def detect_face(img):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img, 1.2, 5)

    if faces == ():
        return False
    else:
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

def take_pic():
    global count

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        if faces == ():
            label1.config(text="Can't identify your face. Please get closer and make sure there is red rectangular araund your face.")
            return False
        else:
            for (x, y, w, h) in faces:

                crop_img = gray[y:y+h, x:x+w]
                count += 1
                cv2.imwrite(newpath+"/User_" + str(id_input) + '.' + str(count) + ".jpg", crop_img)
                print(count)

        time.sleep(0)
        if count == 50:
            label1.config(text="Please smile and capture.")
            count += 1
            return False
        elif count == 100:
            label1.config(text="Please take of glasses if it is exist and capture.")
            count += 1
            return False
        elif count == 150:
            label1.config(text="Please try to draw circle with your head")
            count += 1
            return False
        elif count > 200:
            label1.config(text="Done! You can close the program.")
            train_faces()
            return False

def train_faces():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    get_imagePath = [os.path.join(newpath,f) for f in os.listdir(newpath)]
    faceSamples = []
    ids = []

    for imagePath in get_imagePath:

        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:

            faceSamples.append(img_numpy[y:y+h,x:x+w])

            ids.append(id)

    recognizer.train(faceSamples, np.array(ids))
    recognizer.save('trained/'+id_input+'.yml')

def show_frame():
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    detect_face(rgb)

    prevImg = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def create_path():
    global newpath, id_input, label1, button

    if not os.path.exists('trained/') and not os.path.exists('face_data/'):
        os.makedirs('trained/')
        os.makedirs('face_data/')

    button_path.pack_forget()
    label1 = tk.Label(mainWindow, text="Please capture when you ready!", relief=tk.GROOVE)
    button = tk.Button(mainWindow, text="Capture", command=take_pic)
    label1.pack(side="left")
    button.pack(side="right")
    id_input = id_path.get()              #input
    newpath = r'face_data/' + id_input    #face_data/input
    if not os.path.exists(newpath):
        os.makedirs(newpath)

mainWindow = tk.Tk(screenName="Camera Capture")
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())

id_path = tk.StringVar()

lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
button_path = tk.Button(mainWindow, text="Get new id", command=create_path)
entry = tk.Entry(mainWindow, textvariable = id_path)

entry.pack()
button_path.pack()
lmain.pack()

show_frame()
mainWindow.mainloop()