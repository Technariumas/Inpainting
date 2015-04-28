#Uses inpaint.py largely based on Davide Lasagna's code: https://github.com/gasagna/openpiv-python/blob/master/openpiv/src/lib.pyx
from __future__ import division
import numpy as np
from scipy import ndimage
from inpaint import *
import matplotlib.pyplot as plt


def inpaint_array(inputArray, mask, outputArray):
	maskedImg = np.ma.array(inputArray, mask = mask)
	NANMask =  maskedImg.filled(np.NaN)
	badArrays, num_badArrays = ndimage.label(mask)
	data_slices = ndimage.find_objects(badArrays)
	filled = replace_nans(NANMask, max_iter=20, tol=0.05, kernel_radius=5, kernel_sigma=2, method='idw')
	np.savetxt(outputArray, filled)
	return filled


mask = np.zeros((40, 40))
mask[15:21, 18:21]=1
inputArray = makeGaussian(40, 15)/np.max(makeGaussian(40, 8))
print inputArray, mask, np.sum(mask)
#plt.imshow(mask)
#plt.show()
d = inpaint_array(inputArray, mask, 'out.csv')
c = plt.imshow(d)
plt.colorbar(c)	
plt.show()
