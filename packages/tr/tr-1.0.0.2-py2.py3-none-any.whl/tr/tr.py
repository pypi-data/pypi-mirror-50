# coding: utf-8
import numpy
from PIL import Image
import os
import ctypes
try:
    from .char_table import char_table
except:
    from char_table import char_table

FLAG_RECT = (1 << 0)
FLAG_ROTATED_RECT = (1 << 1)
FLAG_CRNN_PROB = (1 << 16)
FLAG_CRNN_INDEX = (1 << 17)

_BASEDIR = os.path.dirname(os.path.abspath(__file__))

_libc = ctypes.cdll.LoadLibrary(os.path.join(_BASEDIR, 'libtr.so'))
assert _libc is not None

_libc.tr_init.restype = ctypes.c_int
_libc.tr_detect.argtypes = (ctypes.c_void_p,)

_libc.tr_detect.restype = ctypes.c_int
_libc.tr_detect.argtypes = (ctypes.c_void_p, ctypes.c_void_p,
                            ctypes.c_int, ctypes.c_int)

_libc.tr_read_float.restype = ctypes.c_int
_libc.tr_read_float.argtypes = (ctypes.c_void_p, ctypes.c_int)

_libc.tr_read_int.restype = ctypes.c_int
_libc.tr_read_int.argtypes = (ctypes.c_void_p, ctypes.c_int)

_cwd = os.getcwd()
os.chdir(_BASEDIR)
_libc.tr_init()
os.chdir(_cwd)


def _read(arr, flag):
    if arr.dtype == numpy.int32:
        nbytes = _libc.tr_read_int(
            numpy.ctypeslib.as_ctypes(arr),
            flag)
        return nbytes == arr.nbytes
    elif arr.dtype == numpy.float32:
        nbytes = _libc.tr_read_float(
            numpy.ctypeslib.as_ctypes(arr),
            flag)
        return nbytes == arr.nbytes
    else:
        raise NotImplementedError()


def recognize(img):
    if isinstance(img, str):
        img_pil = Image.open(img).convert("L")
    elif isinstance(img, Image.Image):
        if img.mode != "L":
            img_pil = img.convert("L")
        else:
            img_pil = img
    else:
        raise NotImplementedError()

    new_width = int(img_pil.width * 32 / img_pil.height + 0.5)
    img_pil = img_pil.resize((new_width, 32), Image.BICUBIC)

    img_arr = numpy.asarray(img_pil, dtype="float32") / 255

    size = numpy.array([img_pil.width, img_pil.height], dtype="int32")

    num = _libc.tr_recognize(
        numpy.ctypeslib.as_ctypes(img_arr),
        numpy.ctypeslib.as_ctypes(size),
        2,
    )

    if num <= 0:
        return None, None

    crnn_prob = numpy.zeros((num,), "float32")
    crnn_index = numpy.zeros((num,), "int32")

    if not _read(crnn_prob, FLAG_CRNN_PROB):
        return None, None
    if not _read(crnn_index, FLAG_CRNN_INDEX):
        return None, None

    txt = ""
    prob = 0.
    idx_pre = -1
    count = 0
    for pos in range(num):
        idx = crnn_index[pos]
        if idx > 0:
            if idx != idx_pre:
                txt += char_table[idx]

            # txt += char_table[idx]

            count += 1
            prob += crnn_prob[pos]

        idx_pre = idx

    return txt, prob / max(count, 1)


def detect(img, flag=FLAG_RECT):
    if isinstance(img, str):
        img_pil = Image.open(img).convert("L")
    elif isinstance(img, Image.Image):
        if img.mode != "L":
            img_pil = img.convert("L")
        else:
            img_pil = img
    else:
        raise NotImplementedError()

    img_arr = numpy.asarray(img_pil, dtype="float32") / 255

    size = numpy.array([img_pil.width, img_pil.height], dtype="int32")

    num = _libc.tr_detect(
        numpy.ctypeslib.as_ctypes(img_arr),
        numpy.ctypeslib.as_ctypes(size),
        2,
        flag
    )

    if num <= 0:
        return None

    if flag == FLAG_RECT:
        rect_arr = numpy.zeros((num, 4), "float32")
    elif flag == FLAG_ROTATED_RECT:
        rect_arr = numpy.zeros((num, 5), "float32")
    else:
        raise NotImplementedError(flag)

    if not _read(rect_arr, flag):
        return None

    return rect_arr

def run(img):
    if isinstance(img, str):
        img_pil = Image.open(img).convert("L")
    elif isinstance(img, Image.Image):
        if img.mode != "L":
            img_pil = img.convert("L")
        else:
            img_pil = img
    else:
        raise NotImplementedError()

    rect_arr = detect(img_pil, FLAG_RECT)
    rect_arr = numpy.int0(rect_arr)

    for rect in rect_arr:
        x, y, w, h = rect
        line_pil = img_pil.crop((x - 5, y, x + w + 10, y + h))

        txt, prob = recognize(line_pil)

        # print(txt, prob, w, h, "--")
        print(txt)

        # if "传" in txt:
        #     line_pil.show()
        #     break


if __name__ == "__main__":
    from PIL import Image, ImageDraw

    print(recognize("line.png"))

    img_pil = Image.open("test.jpg")
    MAX_SIZE = 2000
    if img_pil.height > MAX_SIZE or img_pil.width > MAX_SIZE:
        scale = max(img_pil.height / MAX_SIZE, img_pil.width / MAX_SIZE)

        new_width = int(img_pil.width / scale + 0.5)
        new_height = int(img_pil.height / scale + 0.5)
        img_pil = img_pil.resize((new_width, new_height), Image.BICUBIC)

    gray_pil = img_pil.convert("L")

    rect_arr = detect(img_pil, FLAG_RECT)

    print(img_pil.width, img_pil.height)

    img_draw = ImageDraw.Draw(img_pil)
    colors = ['red', 'green', 'blue']
    for i, rect in enumerate(rect_arr):
        x, y, w, h = rect
        img_draw.rectangle(
            (x, y, x + w, y + h),
            outline=colors[i % len(colors)],
            width=2)

    img_pil.show()
    img_pil.save("out.png")

    run(gray_pil)

