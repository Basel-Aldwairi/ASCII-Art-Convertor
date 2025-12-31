from http.client import responses

from PIL import Image
from pathlib import Path
import numpy as np
from io import BytesIO
import requests

ROOT = Path().resolve()
# img_path = ROOT / 'images' / 'hornet.jpg'
#
# custom_img = True

def get_path(custom_img = False, web_image = False):
    img_path = ROOT / 'images' / 'pochita.jpg'

    if custom_img:
        if web_image:
            url = input('Enter the Image URL : \n')
            response = requests.get(url)
            return response


        else:
            try:
                img_path = input('Enter the Image path you want to turn to ASCII : \n')
                return img_path
            except Exception as e:
                print(f'[Error Image path ] : {e}')
                return None
    return img_path

def make_ascii(img_path, inverse_colors = False, down_scale_value = 16, web_image = False, threshold = 128):
    img = None
    try:
        if web_image:
            img = Image.open(BytesIO(img_path.content))
        else:
            img = Image.open(img_path)
    except Exception as e:
        print(f'[Error Opening image] : {e}')
        return


    img_grey = img.convert('L')

    old_size = img.size
    new_size = (old_size[0] // down_scale_value, old_size[1] // down_scale_value)
    img_grey = img_grey.resize(new_size)
    img_mat = np.array(img_grey)

    if inverse_colors:
        img_mat = 255 - img_mat

    img_mat_filtered = np.where(img_mat>threshold,img_mat,0)
    # img_mat_filtered = img_mat
    chars = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,"^`'."""
    new_chars = np.array(list(chars[:-4][::-1]))
    char_len = len(new_chars)

    def get_ascii(x):
        return np.floor((x - threshold - 1) / (np.ceil((255 - threshold) / char_len)) - 1).astype(int)


    img_ascii = np.where(img_mat_filtered>=threshold,new_chars[get_ascii(img_mat_filtered)],'.')

    lines = []
    for line in img_ascii:
        line_list = list(line)
        line_list.append(np.str_('\n'))
        new_line = ''.join(line)
        lines.append(new_line)

    output_path = ROOT / 'images' / 'output.text'

    with open (output_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
            f.write('\n')

    print(f"""
Turned image into ASCII 
Original Image path : {img_path}
Output Text path : {output_path}
""")

img_path = get_path(custom_img=True,web_image=True)
make_ascii(img_path,inverse_colors=True,down_scale_value=8,web_image=True,threshold=192)