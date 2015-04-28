# Original inpainting code by Davide Lasagna https://github.com/gasagna/openpiv-python/blob/master/openpiv/src/lib.pyx
# Cython removed and Gaussian kernel code added by opit (http://technarium.lt)
# Note that the Gaussian kernel has a default standard deviation equal to 3 and is normalised to sum up to 1 to preserve flux, which means that for larger standard deviation you'd have to increase the kernel size to avoid artifacts.
# Matplotlib used for testing only.

from __future__ import division
import numpy as np
from scipy import ndimage
from inpaint import *
import matplotlib.pyplot as plt


def inpaint_array(inputArray, mask):
	maskedImg = np.ma.array(inputArray, mask = mask)
	NANMask =  maskedImg.filled(np.NaN)
	badArrays, num_badArrays = ndimage.label(mask)
	data_slices = ndimage.find_objects(badArrays)
	filled = replace_nans(NANMask, max_iter=20, tol=0.05, kernel_radius=5, kernel_sigma=2, method='idw')
	return filled

def test():
	mask = np.zeros((40, 40))
	mask[15:21, 18:21]=1
	inputArray = makeGaussian(40, 25)/np.max(makeGaussian(40, 8))
	d = inpaint_array(inputArray, mask)
	c = plt.imshow(d, interpolation="None", cmap = plt.cm.cubehelix)
	plt.colorbar(c)	
	plt.savefig('healed_iwd.png')

