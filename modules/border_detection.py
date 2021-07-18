import cv2
import numpy as np


def detect_border(img_path):
    img = cv2.imread(img_path, 1)
    img_blured = cv2.fastNlMeansDenoisingColored(img, None, 20, 20, 7, 21)

    boundaries = [([57, 12, 0], [109, 30, 22])]
    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(img_blured, lower, upper)
        border = cv2.bitwise_and(img_blured, img_blured, mask=mask)

    return border


def detect_contours(img_path):
    border = detect_border(img_path)
    border_gray = cv2.cvtColor(border, cv2.COLOR_BGR2GRAY)

    outside_contours, hierarchy = cv2.findContours(border_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in outside_contours:
        area = cv2.contourArea(cnt)
        if area > 2000:
            np.save(f"temp/{img_path.split('/')[1]}_outside_contours.npy", cnt)

    img_blur = cv2.GaussianBlur(border, (7, 7), cv2.BORDER_DEFAULT)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 21, 21)

    kernel = np.ones((5, 5))
    img_dilation = cv2.dilate(img_canny, kernel, iterations=1)

    inside_contours, hierarchy = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in inside_contours:
        area = cv2.contourArea(cnt)
        if area > 300000:
            np.save(f"temp/{img_path.split('/')[1]}_inside_contours.npy", cnt)
