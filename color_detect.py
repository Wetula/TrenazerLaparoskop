import cv2
import numpy as np
import os
import sys


def detect_red(image):
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([5, 255, 255])
    mask1 = cv2.inRange(image, lower_red, upper_red)

    lower_red = np.array([175, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(image, lower_red, upper_red)

    mask = cv2.bitwise_or(mask1, mask2)

    result = cv2.bitwise_and(image, image, mask=mask)

    return result

def detect_blue(image):
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    mask = cv2.inRange(image, lower_blue, upper_blue)

    result = cv2.bitwise_and(image, image, mask=mask)

    return result


def detect_red_and_blue(image):
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    mask0 = cv2.inRange(image, lower_blue, upper_blue)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([5, 255, 255])
    mask1 = cv2.inRange(image, lower_red, upper_red)

    lower_red = np.array([175, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(image, lower_red, upper_red)

    mask1 = cv2.bitwise_or(mask0, mask1)
    mask = cv2.bitwise_or(mask1, mask2)

    result = cv2.bitwise_and(image, image, mask=mask)
    return result


