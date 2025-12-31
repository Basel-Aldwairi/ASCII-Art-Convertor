from pathlib import Path
import numpy as np
from io import BytesIO
import requests
import cv2
from enum import Enum
from PIL import Image

class Mode(Enum):
    THRESHOLD = 0
    SEGMENTATION = 1

    TEST_IMAGE = 0
    CUSTOM_IMAGE = 1
    WEB_IMAGE = 2


ROOT = Path().resolve()

chars = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,"^`'. """[::-1]
char_len = len(chars)
chars_np = np.array(list(chars))




def get_img(mode= Mode.TEST_IMAGE):
    img = None

    match mode:
        case Mode.TEST_IMAGE:
            img_path = '../images/pochita.jpg'
            img = cv2.imread(img_path)

        case Mode.CUSTOM_IMAGE:
            try:
                img_path = input('Enter the Image path you want to turn to ASCII : \n')
                img = cv2.imread(img_path)

            except Exception as e:
                print(f'[Error Image path ] : {e}')

        case Mode.WEB_IMAGE:
            url = input('Enter the Image URL : \n')
            response = requests.get(url, timeout=10)
            img_pil = Image.open(BytesIO(response.content)).convert('RGB')
            img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_BGR2RGB)

    return img

def get_ascii(x):
    return np.floor((x.astype(float) * (char_len - 1)) / 255).astype(np.uint8)



THRESHOLD = 0
SEGMENTATION = 1

def make_ascii(img_mode, preprocess_mode= Mode.SEGMENTATION, inverse_colors = False, down_scale_value = 16, threshold = 128, padding=True, pad_len = 2, pad_value= 128):

    img = get_img(img_mode)


    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_grey_preprocessed = img_grey.copy()

    if inverse_colors:
        img_grey_preprocessed = 255 - img_grey_preprocessed


    match preprocess_mode:
        case Mode.THRESHOLD:
            img_grey_preprocessed = np.where(img_grey_preprocessed>threshold,img_grey_preprocessed,0)

        case Mode.SEGMENTATION:
            if padding:
                pad = pad_len
                img_grey_preprocessed = cv2.copyMakeBorder(
                    img_grey_preprocessed,
                    pad, pad, pad, pad,
                    cv2.BORDER_CONSTANT,
                    value=pad_value
                )

            edges = cv2.Canny(
                img_grey_preprocessed, 50, 150
            )

            edges_bin = (edges > 0).astype('uint8') * 255
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

            closed = cv2.morphologyEx(edges_bin, cv2.MORPH_CLOSE, kernel, iterations=1)
            contoures, _ = cv2.findContours(
                closed,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            mask_c = np.zeros(img_grey_preprocessed.shape, dtype=np.uint8)
            cv2.drawContours(mask_c, contoures, -1, 255, thickness=cv2.FILLED)
            h, w = img_grey_preprocessed.shape
            mask_c_resize = cv2.resize(mask_c, (w, h))

             # Segmented
            img_grey_preprocessed = cv2.bitwise_and(img_grey_preprocessed, mask_c_resize)
            cv2.normalize(
                img_grey_preprocessed,
                img_grey_preprocessed,
                alpha= 0,
                beta= 255,
                norm_type= cv2.NORM_MINMAX
            )

    h, w = img_grey.shape
    new_h, new_w = int(h // down_scale_value), int(w // down_scale_value)
    img_grey_preprocessed = cv2.resize(img_grey_preprocessed, (new_w, new_h))


    img_ascii = np.where(img_grey_preprocessed != 0,chars_np[get_ascii(img_grey_preprocessed)],' ')

    lines = []
    for line in img_ascii:
        line_list = list(line)
        line_list.append(np.str_('\n'))
        new_line = ''.join(line)
        lines.append(new_line)

    output_path = '../images/output.txt'

    with open (output_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
            f.write('\n')

    print(f"""
Turned image into ASCII 
Output Text path : {output_path}
""")

# make_ascii(img_mode=Mode.WEB_IMAGE, preprocess_mode= Mode.SEGMENTATION, inverse_colors=True,down_scale_value=8,threshold=128, pad_value=0, pad_len=5)
