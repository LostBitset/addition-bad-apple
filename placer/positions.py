from PIL import Image
import numpy as np
from skimage.measure import block_reduce
import cv2

import sys
import random

def get_positions(frame):
    pic = Image.open(f"frames/BadApple_{frame}.jpg", "r")
    img = np.asarray(pic)[:,:,0] / 255
    width = None
    if img.sum() < 5:
        return None
    else:
        width = 1
    counts = 220
    print(f"width = {width}, counts = {counts}")
    ratio = img.sum() / counts
    bs = int((ratio ** 0.5) / 2)
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
                if bs > 1:
                    options.append((r * bs, c * bs))
                else:
                    options.append((r, c))
    print(f"sampling from {len(options)} options")
    result = random.sample(options, counts)
    result.sort(key=lambda x: ((x[0] ** 2) + (x[1] ** 2)) ** 0.5)
    return result

if __name__ == "__main__":
    random.seed(443)
    print(get_positions(50))

