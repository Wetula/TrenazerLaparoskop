import cv2
from datetime import datetime
import os


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        cv2.imshow('Obraz z kamery', img)
        key = cv2.waitKey(1)
        if key == 27:
            break  # Escape wyłącza podgląd
        elif key == ord('s'):  # Czeka na klawisz 's', po czym zapisuje obraz
            date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            if not os.path.exists('snap'):
                os.mkdir('snap')
            cv2.imwrite(os.path.join('snap', date + '.png'), img)
    cv2.destroyAllWindows()


def main():
    show_webcam()


if __name__ == '__main__':
    main()
