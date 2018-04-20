import h5py
from create_field import create_field
import matplotlib.pyplot as plt
import numpy as np


infile = "/Users/rythei/Google Drive/Luminosity/GuideVectorModel/08f65a7829871e9399c38a261cdd8be0-clean.h5"
h5f = h5py.File(infile,'r')
E = h5f['clean_map'][:]
h5f.close()

E_map = E[:385,200:]
plt.imshow(E_map)
plt.show()


X,Y = np.meshgrid(np.flip(np.array(range(E_map.shape[0])),axis=0), np.array(range(E_map.shape[1])))

Xdir, Ydir = create_field(E_map, theta=.5)

print('Original Matrix', E)
#print('X component of vectors', Xdir)
#print('Y component of vectors', Ydir)


plt.quiver(X[::10,::10],Y[::10,::10],Ydir[::10,::10],Xdir[::10,::10])
plt.show()

outfile = "/Users/rythei/Google Drive/Luminosity/GuideVectorModel/08f65a7829871e9399c38a261cdd8be0-field_v1.h5"
file = h5py.File(outfile, 'w')
file.create_dataset('Xdir', data=Xdir)
file.create_dataset('Ydir', data=Ydir)

