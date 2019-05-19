import numpy as np
from PIL import Image
from PIL import ImageFilter


def avg_color(img):
    # Zwraca wartość HSV najczęściej występującego koloru
    img = img.filter(ImageFilter.BLUR)
    img = img.convert('HSV')
    size = img.size
    # img = Image.open(file)
    colors = img.getcolors(size[0]*size[1])
    max_occurrence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] > max_occurrence:
                (max_occurrence, most_present) = c
        return most_present
    except TypeError:
        raise Exception("Too many colors in the image")


def main():
    image = ""
    img = Image.open(image)
    col = avg_color(img)
    print(col)


if __name__ == '__main__':
    main()
