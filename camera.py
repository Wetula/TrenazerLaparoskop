import cv2
from datetime import datetime
import os
from imutils.video import FileVideoStream



def list_cameras():
    valid_cams = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap is None or not cap.isOpened():
            print('Warning: unable to open video source: ', i)
        else:
            valid_cams.append(i)

    return valid_cams


def show_webcam(camera=0, mirror=False):
    cam = cv2.VideoCapture(camera)
    if cam is None or not cam.isOpened():
        print("Invalid camera!")
    else:
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

    cam.release()
    cv2.destroyAllWindows()


def main():
    list_cameras()
    show_webcam(0)


if __name__ == '__main__':
    main()
