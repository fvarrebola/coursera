from matplotlib import pyplot
from numpy.core.numeric import zeros
from numpy.ma.core import floor_divide
from scipy import ndimage
import numpy
import pylab
from scipy.misc.pilutil import imsave
import os

def dumb_average(img_array = None, neighbor_count = None):
    
    (img_array_x_len, img_array_y_len) = img_array.shape
    new_img_array = zeros((img_array_x_len, img_array_y_len))
    
    for img_array_x_idx in range(0, img_array_x_len):
        neighbor_start_x_idx = img_array_x_idx - floor_divide(neighbor_count, 2);
        for img_array_y_idx in range(0, img_array_y_len):
            neighbor_start_y_idx = img_array_y_idx - floor_divide(neighbor_count, 2);
            sum = 0
            for neighbor_x_idx in range(neighbor_start_x_idx, neighbor_start_x_idx + neighbor_count):
                for neighbor_y_idx in range(neighbor_start_y_idx, neighbor_start_y_idx + neighbor_count):
                    sum += img_array[neighbor_x_idx % img_array_x_len][neighbor_y_idx % img_array_y_len]
            new_img_array[img_array_x_idx, img_array_y_idx] = floor_divide(sum, (neighbor**2))

    return new_img_array

print ('********************************************************************************')
print ('* Performing a neighborhood avarage                                            *')
print ('********************************************************************************')
import sys
sys.path.append('../utils')
import userinput
fpath = userinput.get_img_path()
img_array = userinput.get_gray_img(fpath)

for neighbor in [3, 10, 20]:
    print ('building new image using \'' + str(neighbor) + '\' neighbors avarage...')
    new_img_array = dumb_average(img_array, neighbor)
    new_fpath = '%s/%i-neighbors-%s' % (os.path.dirname(fpath), neighbor, os.path.basename(fpath))
    print ('saving new image to \'' + new_fpath + '\'...')
    imsave(new_fpath, new_img_array)
    
print ('********************************************************************************')
