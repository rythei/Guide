import h5py
import matplotlib.pyplot as plt
import numpy as np

infile = "/Users/rythei/Google Drive/Luminosity/GuideVectorModel/08f65a7829871e9399c38a261cdd8be0-field_v0.h5"
h5f = h5py.File(infile,'r')
Xdir = h5f['Xdir'][:]
Ydir = h5f['Ydir'][:]
h5f.close()

nrow = Xdir.shape[0]
ncol = Xdir.shape[1]

X,Y = np.meshgrid(np.arange(0,ncol),np.arange(0,nrow))
U = Xdir
V = Ydir


print(X.shape)
print(Y.shape)
print(U.shape)
print(V.shape)

plt.quiver(Y[::10,::10],X[::10,::10],V[::10,::10],U[::10,::10],units='width')
plt.show()
