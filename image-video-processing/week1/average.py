from scipy import ndimage
import numpy
import pylab
from numpy.ma.core import floor_divide
from numpy.core.numeric import zeros
from matplotlib import pyplot

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

fpath = raw_input('> image\'s full path:')
try:
   with open(fpath) as f: pass
except IOError as e:
   print (fpath + ' could not be opened')

# reads the image using ndimage.imread()...
print ('\treading image...')
img = ndimage.imread(fpath)
img_array = numpy.array(img)

for neighbor in [3, 10, 20]:
    
    print ('\tbuilding new image using \'' + str(neighbor) + '\' neighbors avarage...')
    new_img_array = dumb_average(img_array, neighbor)
    
    new_fpath = '%s-%s.jpg' % (fpath, str(neighbor))
    print ('\t\tsaving new image to \'' + new_fpath + '\'...')
    pyplot.imsave(new_fpath, new_img_array, cmap='gray', format='png')
    
print ('********************************************************************************')