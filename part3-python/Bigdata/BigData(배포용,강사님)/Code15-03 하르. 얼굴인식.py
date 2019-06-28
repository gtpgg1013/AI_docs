import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")

frame = cv2.imread('C:/images/images(ML)/02twice.jpg')
grey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

# 얼굴이 여러개일 경우엔 여러개를 찾아줌. 얼굴위치 사각형 [ [x1,y1,w,h], [x1,y1,w,h],... ]
face_rects = face_cascade.detectMultiScale(grey, 1.1, 5)
print(face_rects)
for  (x,y,w,h) in face_rects :
    cv2.rectangle(frame, (x,y), (x+w, y+w), (0,255,0), 3)

cv2.imshow('', frame)
c =cv2.waitKey()
cv2.destroyAllWindows()