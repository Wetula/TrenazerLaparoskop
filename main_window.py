from tkinter import Tk, Frame, Label, Menu
from PIL import Image
from PIL import ImageTk
import threading
import imutils
import cv2
from get_video import GetVideo
from show_video import ShowVideo
from color_detect import detect_red, detect_blue


def main():
    window = Tk()
    window.title("Trenażer operacji laparoskopowej")

    image_frame = Frame(window, width=600, height=500)
    image_frame.grid(row=0, column=0, padx=10, pady=2)

    source = 1
    cap = GetVideo(source).start()

    main_label = Label(image_frame)
    main_label.grid(row=0, column=0)

    def show_frame():
        frame = cap.frame
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

    menu = Menu(window)
    menu_item = Menu(menu, tearoff=0)
    menu_item.add_command(label='New')
    # menu_item.add_separator()
    menu_item.add_command(label='Edit')
    menu.add_cascade(label='File', menu=menu_item)

    # my_canvas = Canvas(window, width=cap.width(), height=cap.height())
    #  my_canvas.pack()

    window.config(menu=menu)
    show_frame()
    window.mainloop()
    cap.stop()


if __name__ == "__main__":
    main()
