import numpy as np
import cv2
import requests
from io import BytesIO
from PIL import Image

url = 'https://media.gettyimages.com/id/1459780477/vector/heart.jpg?s=612x612&w=gi&k=20&c=xKg93BkBwGYYgheH-zDROpQNYiSD59wFnAxgPtz_lDA='

response = requests.get(url)
r_ = Image.open(BytesIO(response.content)).convert('RGB')
img = cv2.cvtColor(np.array(r_), cv2.COLOR_RGB2BGR)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
