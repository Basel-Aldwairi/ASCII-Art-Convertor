from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
img_path = ROOT / 'images' / 'hornet.jpg'

img = Image.open(img_path)


mat = img.convert(matrix=(200,200))
# print(list(mat))