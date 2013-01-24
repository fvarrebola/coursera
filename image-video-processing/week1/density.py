from matplotlib import pyplot
from scipy import ndimage
import numpy
from numpy.ma.core import floor

print ('********************************************************************************')
print ('* Changing the intensity levels of an image using SciPy, NumPy and MatPlotLib  *')
print ('********************************************************************************')

fpath = raw_input('> image\'s full path:')
try:
   with open(fpath) as f: pass
except IOError as e:
   print (fpath + ' could not be opened')

# reads the image using ndimage.imread()...
print ('\treading image...')
img = ndimage.imread(fpath)
img_array = numpy.array(img)

# builds new images...
intensities = [2, 4, 8, 16, 32, 64, 128, 255];
for intensity in intensities: 
    print ('\tbuilding new image using an intensity level of \'' + str(intensity) + '\'...')
    new_img_array = floor(numpy.array(img_array) / intensity) * intensity
    new_fpath = fpath + '-' + str(intensity) + '.png'
    print ('\t\tsaving new image to \'' + new_fpath + '\'...')
    pyplot.imsave(new_fpath, new_img_array, cmap='gray', format='png')

print ('********************************************************************************')