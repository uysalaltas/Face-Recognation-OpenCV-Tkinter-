# Author : Uysal Altas
# Date   : 08/2018

import cv2
import os

cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX

path = 'trained/'

for i in os.listdir(path):
    recognizer.read(path + i)
    print(i)

while True:
    flag, im = cap.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        cv2.circle(im, (x+int(w/2), y+int(h/2)), 100, (0, 0, 255), 0)
        Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        Id = "User {0:.2f}%".format(round(100 - confidence, 2))

        if float("{0:.2f}".format(round(100 - confidence, 2))) > 50:
            cv2.putText(im, str(Id), (x, y - 40), font, 1, (255, 255, 255), 3)
        else:
            cv2.putText(im, "Not found!", (0, 30), font, 1, (255, 0, 0), 2)

    cv2.imshow('im',im)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()