import cv2
import os
import numpy as np
import argparse

def detect_face(img):
    #gray = img#cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)
    print(faces)


parser = argparse.ArgumentParser(description ='Haex da best. Exit with ESC')
parser.add_argument('--face_cascade', help='Path to face cascade (On ubuntu after install opencv-data /usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml')
parser.add_argument('--image', help='Path to RGB image with faces')
args = parser.parse_args()
face_cascade_name = args.face_cascade
face_cascade = cv2.CascadeClassifier()
if not face_cascade.load(face_cascade_name):
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
