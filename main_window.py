from tkinter import Tk, Frame, Label, Menu, messagebox, Toplevel, Listbox, Button
from PIL import Image
from PIL import ImageTk
import threading
import imutils
import cv2
from get_video import GetVideo
from show_video import ShowVideo
from color_detect import detect_red, detect_blue
import numpy as np


class Frames(object):

    def __init__(self):
        self.root = Tk()
        self.pick_window = Toplevel()
        self.cal_window = Toplevel()
        self.valid_cams = []
        self.source = 0
        self.cap = cv2.VideoCapture
        self.mtx = []
        self.dist = []
        self.cal_frame = []
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_source(self, x):
        self.source = x

    def on_closing(self):
        if messagebox.askokcancel("Wyjście", "Czy chcesz wyłączyć aplikację?"):
            self.cap.stop()
            self.root.destroy()
            cv2.destroyAllWindows()

    def list_cameras(self):
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap is None or not cap.isOpened():
                pass
            else:
                self.valid_cams.append(int(i))
                cap.release()

    def pick_camera(self):
        def on_select(evt):
            w = evt.widget
            index = w.curselection()[0]
            value = w.get(index)
            app.set_source(x=value)

        pick_window = self.pick_window
        pick_window.title("Wybór źródła")
        pick_window.attributes("-topmost", True)
        pick_window.grab_set()

        label = Label(pick_window, text="Wybierz kamerę, której chcesz używać.")
        label.pack()

        listbox = Listbox(pick_window, selectmode='single')
        listbox.bind('<<ListboxSelect>>', on_select)
        for i in self.valid_cams:
            listbox.insert(10, i)

        button = Button(pick_window, text="Wybierz", command=pick_window.destroy)

        listbox.pack()
        button.pack()
        self.root.wait_window(pick_window)
        # print(self.source)

    def get_cal_frame(self):
        cap = GetVideo(self.source).start()

        def take_shot():
            cap.stop()
            app.cal_frame = cap.frame

        def show_frame():
            frame = cap.frame

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            img_tk = ImageTk.PhotoImage(image=img)
            main_label.imgtk = img_tk
            main_label.configure(image=img_tk)
            main_label.after(10, show_frame)

        cal_window = self.cal_window
        cal_window.title("Kalibracja kamery")
        cal_window.attributes("-topmost", True)
        cal_window.grab_set()
        main_label = Label(cal_window)
        # main_label.pack()

        label1 = Label(cal_window, text="Zrób ujęcie szachownicy kalibracyjnej.")
        label2 = Label(cal_window, text="Postaraj się, by wypełniła cały kadr.")
        button1 = Button(cal_window, text="Ujęcie", command=take_shot)
        button2 = Button(cal_window, text="Zamknij", command=cal_window.destroy)
        label1.pack()
        label2.pack()
        main_label.pack()
        button1.pack()
        button2.pack()
        show_frame()

        self.root.wait_window(cal_window)
        cap.stop()
        del cap

    def calibrate_camera(self):

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        objp = np.zeros((9 * 7, 3), np.float32)
        objp[:, :2] = np.mgrid[0:9 * 20:20, 0:7 * 20:20].T.reshape(-1, 2)

        objpoints = []
        imgpoints = []

        img = self.cal_frame

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9, 7), None)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            cv2.drawChessboardCorners(img, (9, 7), corners2, ret)
            # cv2.imshow('img', img)
            # cv2.waitKey(500)
            # cv2.imwrite("chess.png", img)
        # cv2.destroyAllWindows()

        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        h, w = img.shape[:2]
        new_matrix, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w, h), 1, (w, h))

        # undistort
        dst = cv2.undistort(img, self.mtx, self.dist, None, new_matrix)
        # crop the image
        # x, y, w, h = roi
        # dst = dst[y:y + h][ x:x + w]
        cv2.imwrite('calibresult.png', dst)

        # pass
        # TODO: Window to calibrate camera

    def main_window(self):
        # print("MAIN WINDOW STARTING")
        self.root.title("Trenażer operacji laparoskopowej")

        image_frame = Frame(self.root, width=600, height=500)
        image_frame.grid(row=0, column=0, padx=10, pady=2)

        # print("GETTING CAMERA")
        self.cap = GetVideo(self.source).start()
        # print("CAMERA GOT")

        main_label = Label(image_frame)
        main_label.grid(row=0, column=0)

        def show_frame():
            frame = self.cap.frame
            h, w = frame.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(app.mtx, app.dist, (w, h), 1, (w, h))
            frame = cv2.undistort(frame, app.mtx, app.dist, None, newcameramtx)
            # frame = cv2.flip(frame, -1)
            # frame = cv2.GaussianBlur(frame, (9, 9), 0)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # frame = detect_red(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            img_tk = ImageTk.PhotoImage(image=img)
            main_label.imgtk = img_tk
            main_label.configure(image=img_tk)
            main_label.after(10, show_frame)

        menu = Menu(self.root)
        menu_item = Menu(menu, tearoff=0)
        # menu_item.add_command(label='Nowy')
        # menu_item.add_separator()
        # menu_item.add_command(label='Edytuj')
        menu_item.add_command(label='Zamknij')
        menu.add_cascade(label='Plik', menu=menu_item)

        # my_canvas = Canvas(window, width=cap.width(), height=cap.height())
        # my_canvas.pack()
        #
        self.root.config(menu=menu)
        show_frame()

    def __del__(self):
        self.cap.stop()


if __name__ == "__main__":
    app = Frames()
    app.list_cameras()
    app.pick_camera()
    # app.root.wait_window(app.pick_window)

    app.get_cal_frame()
    app.calibrate_camera()
    app.main_window()
    app.root.mainloop()
    del app
