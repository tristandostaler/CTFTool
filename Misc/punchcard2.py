# -*- coding: utf-8 -*-

import sys
import tempfile
import shutil
from PIL import Image


class punch_card_reader:
    """
        Punch car reader for the 80-column card
    """
    matrix1 = {
        -2: "&", -1: "-", 0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9"
    }
    matrix2 = {
        (-2, 1): "a", (-2, 2): "b", (-2, 3): "c", (-2, 4): "d", (-2, 5): "e", (-2, 6): "f", (-2, 7): "g", (-2, 8): "h", (-2, 9): "i",
        (-1, 1): "j", (-1, 2): "k", (-1, 3): "l", (-1, 4): "m", (-1, 5): "n", (-1, 6): "o", (-1, 7): "p", (-1, 8): "q", (-1, 9): "r",
        (0, 1): "/", (0, 2): "s", (0, 3): "t", (0, 4): "u", (0, 5): "v", (0, 6): "w", (0, 7): "x", (0, 8): "y", (0, 9): "z",
        (2, 8): ":", (3, 8): "#", (4, 8): "@", (5, 8): "'", (6, 8): "=", (7, 8): "\"",
        (-2, 2, 8): "¢", (-2, 3, 8): ".", (-2, 4, 8): "<", (-2, 5, 8): "(", (-2, 6, 8): "+", (-2, 7, 8): "|", (-1, 2, 8): "!",
        (-1, 3, 8): "$", (-1, 4, 8): "*", (-1, 5, 8): ")", (-1, 6, 8): ";", (-1, 7, 8): "¬", (0, 2, 8): "≡", (0, 3, 8): "\,",
        (0, 4, 8): "%", (0, 5, 8): "_", (0, 6, 8): ">", (0, 7, 8): "?"
    }

    def getCharacters(self, key):
        global matrix1, matrix2
        if len(key) == 1:
            key = key[0]
        if isinstance(key, int):
            return self.matrix1.get(key)
        elif isinstance(key, list):
            key = tuple(key)
            return self.matrix2.get(key)

    def read(self, file):
        print "reading punch card..."
        picture = Image.open(file)
        # Get the size of the image
        width, height = picture.size

        x_pos = 13
        word = []
        while x_pos < width:
            characters = []

            y_pos = 40
            for i in range(-2, 10):
                current_color = picture.getpixel((x_pos, y_pos))
                if current_color == (0, 0, 0):
                    characters.append(i)
                y_pos += 150
            x_pos += 52

            chars = self.getCharacters(characters)
            if chars is not None:
                word.append(chars)
            else:
                word.append(' ')

        print "\n{} characters found".format(len(word))
        print word
        return ("".join(word)).replace('\\,', ',')


def remove_noise(img_in):
    print "Removing noise..."
    img_out = "{}\{}".format(tmp_dir, "simple.tif")
    picture = Image.open(img_in)

    # Get the size of the image
    width, height = picture.size

    # Process every pixel
    for y in range(height):
        x = 0
        while x < width:
            current_color = picture.getpixel((x, y))

            if current_color != (0, 0, 0):  # if not black
                picture.putpixel((x, y), (255, 255, 255))  # then replace by white
            else:
                for z in range(24):
                    p = x + z
                    if p < width:
                        picture.putpixel((p, y), (0, 0, 0))
                x = p + 10
            x += 1

    picture.save(img_out, "TIFF")
    # print "Clean picture build : %s" % img_out
    return img_out



def doCrop(imagePath,  x, y, x2, y2):
    print "Crop..."
    img_out = "{}\{}".format(tmp_dir, "cropped.tif")
    im = Image.open(imagePath)
    box = (x, y, x2, y2)
    region = im.crop(box)   # extract the box region
    region.save(img_out, "TIFF")   # save it as a separate image
    return img_out

if __name__ == '__main__':
    # print ocr(sys.argv[1])

    global tmp_dir
    tmp_dir = tempfile.mkdtemp(prefix="punch_card")

    card_path = sys.argv[1]
    croped = doCrop(card_path, 140, 130, 2990, 1860)
    cleaned = remove_noise(croped)

    words = punch_card_reader().read(cleaned)
    print "text : %s" % words
    shutil.rmtree(tmp_dir)
