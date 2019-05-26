from tkinter import Tk, Frame, Label, Menu, messagebox
from PIL import Image
from PIL import ImageTk
import threading
import imutils
import cv2
from get_video import GetVideo
from show_video import ShowVideo
from color_detect import detect_red, detect_blue


class Frames(object):

    def __init__(self):
        self.root = Tk()
        self.valid_cams = []
        self.source = 1
        self.cap = cv2.VideoCapture
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if messagebox.askokcancel("Wyjście", "Czy chcesz wyłączyć aplikację?"):
            self.cap.stop()
            self.root.destroy()

    def list_cameras(self):
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap is None or not cap.isOpened():
                print('Warning: unable to open video source: ', i)
            else:
                self.valid_cams.append(i)

    def pick_camera(self):
        pass
        # TODO: Window with camera list

    def main_window(self):
        self.root.title("Trenażer operacji laparoskopowej")

        image_frame = Frame(self.root, width=600, height=500)
        image_frame.grid(row=0, column=0, padx=10, pady=2)

        self.cap = GetVideo(self.source).start()

        main_label = Label(image_frame)
        main_label.grid(row=0, column=0)

        def show_frame():
            frame = self.cap.frame
            frame = cv2.flip(frame, 1)
            frame = cv2.GaussianBlur(frame, (9, 9), 0)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame = detect_red(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            img_tk = ImageTk.PhotoImage(image=img)
            main_label.imgtk = img_tk
            main_label.configure(image=img_tk)
            main_label.after(10, show_frame)

        menu = Menu(self.root)
        menu_item = Menu(menu, tearoff=0)
        menu_item.add_command(label='New')
        # menu_item.add_separator()
        menu_item.add_command(label='Edit')
        menu.add_cascade(label='File', menu=menu_item)

        # my_canvas = Canvas(window, width=cap.width(), height=cap.height())
        #  my_canvas.pack()

        self.root.config(menu=menu)
        show_frame()
        # cap.stop()

    def __del__(self):
        self.cap.stop()


if __name__ == "__main__":
    app = Frames()
    app.main_window()
    app.root.mainloop()
    del app
