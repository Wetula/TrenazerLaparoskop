import color_detect
import camera
import cv2


def play_video():
    vid = cv2.VideoCapture('test_red.mp4')
    while True:
        ret, frame = vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame = color_detect.detect_red(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    """ This is executed when run from the command line """

    play_video()
