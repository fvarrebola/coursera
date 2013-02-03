from matplotlib import pyplot
from scipy import ndimage
import numpy
from numpy.ma.core import floor
from string import replace
from scipy.misc.pilutil import imsave
import os


print ('********************************************************************************')
print ('* Changing the intensity levels of an image using SciPy, NumPy and MatPlotLib  *')
print ('********************************************************************************')
import sys
sys.path.append('../utils')
import userinput
fpath = userinput.get_img_path()
img_array = userinput.get_gray_img(fpath)

# builds new images...
intensities = [2, 4, 8, 16, 32, 64, 128, 255];
for intensity in intensities: 
    print ('building new image using an intensity level of \'' + str(intensity) + '\'...')
    new_img_array = floor(numpy.array(img_array) / intensity) * intensity
    new_fpath = '%s/%i-intensity-%s' % (os.path.dirname(fpath), intensity, os.path.basename(fpath))
    print ('saving new image to \'' + new_fpath + '\'...')
    imsave(new_fpath, new_img_array)

print ('********************************************************************************')