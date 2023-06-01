from PIL import Image
import numpy as np
from skimage.measure import block_reduce
import cv2

import sys
import random

random.seed(443)

frame = int(sys.argv[1])

pic = Image.open(f"frames/BadApple_{frame}.jpg", "r")
img = np.asarray(pic)[:,:,0] / 255

area = img.sum() / img.size

width = None
if area < 0.005:
    print("nothing")
    sys.exit(0)
else:
    width = 1

counts = 220

density = counts / area
bs = int((density ** 0.5) / 2)

if bs > 1:
    img = block_reduce(
        img,
        block_size=(bs, bs),
        func=np.mean,
    )
img = img > 0.01

options = []
for r, row in enumerate(img):
    for c, entry in enumerate(row):
        if entry:
            options.append((r * bs, c * bs))

print(options)

