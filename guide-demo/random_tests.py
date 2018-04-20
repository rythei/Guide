from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

def load_image(infilename):
    img = Image.open(infilename)
    img.load()
    data = np.asarray(img, dtype="float32")
    return data

sample_im = "sample_map.png"
map2d = load_image(sample_im)

plt.imshow(map2d[:,:,2])
plt.show()