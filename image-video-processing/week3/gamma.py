from scipy.misc.pilutil import imsave
import numpy
import sys
from numpy.ma.core import exp
import os

print ('********************************************************************************')
print ('* Really simple gamma correction                                               *')
print ('********************************************************************************')
sys.path.append('../utils')
import userinput
fpath = userinput.get_img_path()
img_array = userinput.get_gray_img(fpath)
(img_array_x_len, img_array_y_len) = img_array.shape

const = 1
for gamma in [0.03, 0.10, 0.20, 0.40, 0.67, 1.0, 1.5, 2.5, 5.0, 10.0, 25.0]:
    new_img_array = const * numpy.power(img_array, gamma)
    new_path = '%s/%i-%f-intensity-%s' % (os.path.dirname(fpath), const, gamma, os.path.basename(fpath))
    print 'saving grayscale negative image as \'%s\'...' % (new_path)
    imsave(new_path, new_img_array)
print ('********************************************************************************')
