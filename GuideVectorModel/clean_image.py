from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import h5py

def load_image(infilename):
    img = Image.open(infilename)
    img.load()
    data = np.asarray(img, dtype="int32")
    return data

#pull in image
sample_im = "/Users/rythei/Google Drive/Luminosity/GuideVectorModel/08f65a7829871e9399c38a261cdd8be0-edit3.png"
img = load_image(sample_im)

#this particular channel seems to contain all the information we need
slice_im = img[:,:,1]
print('Distinct color values in slice', np.unique(slice_im))

### in this image, pixel values of 200 correspond to open space, 0 correspond to hazards, 255 are boundaries, 185 is the path,
### and all other values are along the weird edge of the image

clean_im = np.zeros(slice_im.shape)
clean_im[slice_im == 185] = 1
clean_im[slice_im == 200] = 0
clean_im[slice_im == 255] = -1
clean_im[slice_im == 0] = -1

outfile = "/Users/rythei/Google Drive/Luminosity/GuideVectorModel/08f65a7829871e9399c38a261cdd8be0-clean.h5"
file = h5py.File(outfile, 'w')
file.create_dataset('clean_map', data=clean_im)

## plot cleaned image
#plt.imshow(clean_im)
#plt.colorbar()
#plt.show()