# Original inpainting code by Davide Lasagna https://github.com/gasagna/openpiv-python/blob/master/openpiv/src/lib.pyx
# Cython removed and Gaussian kernel code added by opit (https://github.com/astrolitterbox)
# Note that the Gaussian kernel has a default standard deviation equal to 3 and is normalised to sum up to 1 to preserve flux, which means that for larger standard deviation you'd have to increase the kernel size.


from __future__ import division
import numpy as np
from scipy.stats import multivariate_normal

def makeGaussian(size, sigma):
	x, y = np.mgrid[0:size:1, 0:size:1]
	pos = np.empty(x.shape + (2,))
	pos[:, :, 0] = x; pos[:, :, 1] = y
	rv = multivariate_normal(mean=[size/2,size/2], cov=[[sigma,0],[0,sigma]])
	return rv.pdf(pos)/np.sum(rv.pdf(pos))

def replace_nans(array, max_iter=50, tol=0.05, kernel_radius=2, kernel_sigma=2, method='idw'):
	"""Replace NaN elements in an array using an iterative image inpainting algorithm.
	The algorithm is the following:
	1) For each element in the input array, replace it by a weighted average
	of the neighbouring elements which are not NaN themselves. The weights depends
	of the method type. If ``method=localmean`` weight are equal to 1/( (2*kernel_size+1)**2 -1 )
	2) Several iterations are needed if there are adjacent NaN elements.
	If this is the case, information is "spread" from the edges of the missing
	regions iteratively, until the variation is below a certain threshold.
	Parameters
	----------
	array : 2d np.ndarray
	an array containing NaN elements that have to be replaced
	max_iter : int
	the number of iterations
	kernel_size : int
	the size of the kernel, default is 1
	method : str
	the method used to replace invalid values. Valid options are
	`localmean`, 'idw'.
	Returns
	-------
	filled : 2d np.ndarray
	a copy of the input array, where NaN elements have been replaced.
	"""
	kernel_size = kernel_radius*2+1
	filled = np.empty( [array.shape[0], array.shape[1]])
	kernel = np.empty( (2*kernel_size+1, 2*kernel_size+1))
	
	# indices where array is NaN
	inans, jnans = np.nonzero( np.isnan(array) )
	
	# number of NaN elements
	n_nans = len(inans)
	
	# arrays which contain replaced values to check for convergence
	replaced_new = np.zeros( n_nans)
	replaced_old = np.zeros( n_nans)
	
	# depending on kernel type, fill kernel array
	if method == 'localmean':
	  
		print 'kernel_size', kernel_size	   
		for i in range(kernel_size):
			for j in range(kernel_size):
				kernel[i,j] = 1
		print kernel, 'kernel'

	elif method == 'idw':
		kernel = makeGaussian(kernel_size, kernel_sigma)
		print kernel.shape, 'kernel'	  
	else:
		raise ValueError( 'method not valid.')
	
	# fill new array with input elements
	for i in range(array.shape[0]):
		for j in range(array.shape[1]):
			filled[i,j] = array[i,j]

	# make several passes
	# until we reach convergence
	for it in range(max_iter):
		print 'iteration', it
		# for each NaN element
		for k in range(n_nans):
			i = inans[k]
			j = jnans[k]
			
			# initialize to zero
			filled[i,j] = 0.0
			n = 0
			
			# loop over the kernel
			for I in range(kernel_size):
				for J in range(kernel_size):
				   
					# if we are not out of the boundaries
					if i+I-kernel_radius < array.shape[0] and i+I-kernel_radius >= 0:
						if j+J-kernel_radius < array.shape[1] and j+J-kernel_radius >= 0:
												
							# if the neighbour element is not NaN itself.
							if filled[i+I-kernel_radius, j+J-kernel_radius] == filled[i+I-kernel_radius, j+J-kernel_radius] :
								
								# do not sum itself
								if I-kernel_radius != 0 and J-kernel_radius != 0:
									
									# convolve kernel with original array
									filled[i,j] = filled[i,j] + filled[i+I-kernel_radius, j+J-kernel_radius]*kernel[I, J]
									n = n + 1*kernel[I,J]
									print n

			# divide value by effective number of added elements
			if n != 0:
				filled[i,j] = filled[i,j] / n
				replaced_new[k] = filled[i,j]
			else:
				filled[i,j] = np.nan
				
		# check if mean square difference between values of replaced
		#elements is below a certain tolerance
		print 'tolerance', np.mean( (replaced_new-replaced_old)**2 )
		if np.mean( (replaced_new-replaced_old)**2 ) < tol:
			break
		else:
			for l in range(n_nans):
				replaced_old[l] = replaced_new[l]
	return filled


