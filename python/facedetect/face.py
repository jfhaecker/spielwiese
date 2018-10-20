import cv2
print("OpenCV Version: "+cv2.__version__)
import os
import numpy as np
import argparse

def detect_face(img):
    #gray = img#cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, scaleFactor=myscaleFactor, minNeighbors=myminNeighbors)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)


parser = argparse.ArgumentParser(description ='Haex da best. Exit with ESC')
parser.add_argument('--face_cascade', help='Path to face cascade (On ubuntu after install opencv-data /usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml')
parser.add_argument('--image', help='Path to RGB image with faces')
parser.add_argument('--scaleFactor', help="See OpenCV Doc for details. Default 1.2", default=1.2, type=float)
parser.add_argument('--minNeighbors', help="See OpenCV Doc for details. Default 5 ", default=5, type=int)         

args = parser.parse_args()

face_cascade_name = args.face_cascade
myscaleFactor = args.scaleFactor
myminNeighbors = args.minNeighbors
print(str(myminNeighbors)+" "+str(myscaleFactor))


face_cascade = cv2.CascadeClassifier()
if not face_cascade.load(face_cascade_name, ):
    print("Error loading face cascade")
    exit()
image_name = args.image
img = cv2.imread(image_name, 0)
if img.all() == None:
    raise Exception("could not load image")

detect_face(img)
while(1):
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image", 800, 600)
    cv2.imshow("Image", img)
    c = cv2.waitKey(0)
    if c == 27:
        print("Ende Gelände")
        cv2.destroyAllWindows()
        break
    continue
