import numpy as np
from skimage.measure import block_reduce
import cv2

import sys
import random

def get_positions(frame, counts):
    path = f"frames/BadApple_{frame}.jpg"
    print(path)
    rgb = cv2.imread(path)
    img = rgb[:,:,0]
    img = img > 100
    print(f"original image has ~{int(img.sum())} white pixels")
    if img.sum() < 5:
        return None
    print(f"(using) counts = {counts}")
    ratio = img.sum() / counts
    print(f"ratio = {ratio:.2f}")
    bs = int((ratio ** 0.5) * (4 / 5))
    print(f"ideal block size {bs}")
    if bs < 10:
        bs = 10
    print(f"using block size {bs}")
    print(f"original image size {img.size}")
    img = block_reduce(
        img,
        block_size=(bs, bs),
        func=np.mean,
    )
    print(f"reduced image size {img.size}")
    img = img > 0.01
    options = []
    for r, row in enumerate(img):
        for c, entry in enumerate(row):
            if entry:
                if bs != 0:
                    options.append((r * bs, c * bs))
                else:
                    options.append((r, c))
    print(f"sampling from {len(options)} options")
    result = random.sample(options, counts)
    result.sort(key=lambda x: ((x[0] ** 2) + (x[1] ** 2)) ** 0.5)
    return result

if __name__ == "__main__":
    random.seed(443)
    print(get_positions(int(sys.argv[1]), 220))

