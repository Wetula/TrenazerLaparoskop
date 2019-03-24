import cv2
import numpy as np


def detect_red(image):
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([5, 255, 255])
    mask1 = cv2.inRange(image, lower_red, upper_red)

    lower_red = np.array([175, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(image, lower_red, upper_red)

    mask = cv2.bitwise_or(mask1, mask2)

    result = cv2.bitwise_and(image, image, mask=mask)
    result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    cv2.waitKey()
    cv2.destroyAllWindows()


def detect_blue(image):
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    mask = cv2.inRange(image, lower_blue, upper_blue)

    result = cv2.bitwise_and(image, image, mask=mask)
    result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    cv2.waitKey()


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
    result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    cv2.waitKey()


def menu():
    image = cv2.imread('pills.jpg', cv2.IMREAD_UNCHANGED)
    # image = cv2.imread('tester.png', cv2.IMREAD_UNCHANGED)
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    print('Pick operation')
    print('B - Detect blue')
    print('R - Detect red')
    print('D - Detect both')
    pick = input('Pick: ')
    if pick == 'B' or pick == 'b':
        detect_blue(img_hsv)
    elif pick == 'R' or pick == 'r':
        detect_red(img_hsv)
    elif pick == 'D' or pick == 'd':
        detect_red_and_blue(img_hsv)
    else:
        print('Wrong input.')


if __name__ == "__main__":
    """ This is executed when run from the command line """
    menu()
