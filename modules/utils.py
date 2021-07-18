import cv2
import os
import pickle
import numpy as np


def create_classes(database_path):
    classes = []
    
    for expansion in os.listdir(f"{database_path}/stock_images"):
        for card in os.listdir(f"{database_path}/stock_images/{expansion}"):
            classes.append(card)

    with open(f"{database_path}/classes.txt", "wb+") as file:
        pickle.dump(classes, file)


def get_cropped_card(img_path, fx=1/6, fy=1/6):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (0, 0), fx=fx, fy=fy)

    img_blur = cv2.GaussianBlur(img, (7, 7), cv2.BORDER_DEFAULT)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 21, 43)

    kernel = np.ones((5, 5))
    img_dilation = cv2.dilate(img_canny, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(contour, (x, y), (x + w, y + h), (0, 255, 0), 5)

    cropped_card = img[y:y+h, x:x+w]

    return cropped_card


def load_classes(classes_path):
    with open(classes_path, "rb") as file:
        classes = pickle.load(file)
        
    return classes
