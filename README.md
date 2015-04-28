Inpainting
Healing holes in Python arrays with inverse-distance weighted Gaussian kernel or a local mean.

Original inpainting code (the replace_nans function) by Davide Lasagna https://github.com/gasagna/openpiv-python/blob/master/openpiv/src/lib.pyx

Cython removed and Gaussian kernel code added by opit (https://github.com/astrolitterbox)

Note that the Gaussian kernel has a default standard deviation equal to 3 and is normalised to sum up to 1 to preserve flux, which means that for larger standard deviation you'd have to increase the kernel size to avoid artifacts.

A cleaned-up old script someone nevertheless found useful: http://astrolitterbox.blogspot.it/2012/03/healing-holes-in-arrays-in-python.html?showComment=1429681165434#c8748278569963349180

See the test() function in inpaint_array.py for an example.
