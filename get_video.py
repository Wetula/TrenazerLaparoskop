from threading import Thread
import cv2


class GetVideo:

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True

    def width(self):
        w = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        return w

    def height(self):
        h = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return h
