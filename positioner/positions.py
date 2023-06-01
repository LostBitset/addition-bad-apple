from PIL import Image
import numpy as np

import sys

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
bs = int(density ** 0.5)
print(bs)

