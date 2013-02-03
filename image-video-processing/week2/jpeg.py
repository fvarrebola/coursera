from copy import copy
from matplotlib import pyplot
from numpy.core.numeric import zeros
from numpy.ma.core import cos, floor, sqrt, size
from numpy.numarray.functions import reshape, round
from scipy import ndimage
from scipy.constants.constants import pi
from scipy.misc.pilutil import imsave
import numpy

centering_factor = 128

# DCT alphas and cosines
alphas_table = zeros((8, 8))
cosines_table = zeros((8, 8))

# quantization block
q1 = [[16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]]
quantization_array = numpy.array(q1)

sqrt_1_8 = 0.353553390593  # sqrt(1/8.)
sqrt_1_4 = .5  # sqrt(1/4.)
def alpha(i): 
    return sqrt_1_8 if (i == 0) else sqrt_1_4

def build_alphas_table():
    for u_v_idx, u_v in numpy.ndenumerate(alphas_table):
        (u, v) = u_v_idx
        alphas_table[u, v] = alpha(u) * alpha(v) 
    return

pi_over_8 = 0.39269908169872414  # pi / 8
def build_cosines_table():
    for index, v in numpy.ndenumerate(alphas_table):
        (x, y) = index
        cosines_table[x, y] = cos(pi_over_8 * (x + .5) * y)
    return

def dct(array):
    build_alphas_table()
    build_cosines_table()
    centered_array = array - centering_factor
    dct_array = zeros(centered_array.shape)
    for u_v_idx, u_v in numpy.ndenumerate(dct_array):
        (u, v) = u_v_idx
        dct = 0
        for x_y_idx, x_y in numpy.ndenumerate(centered_array):
            (x, y) = x_y_idx
            dct += alphas_table[u, v] * x_y * cosines_table[x, u] * cosines_table[y, v]
        dct_array[u, v] = dct
    return dct_array

def idct(array):
    build_alphas_table()
    build_cosines_table()
    idct_array = zeros(array.shape) 
    for x_y_idx, x_y in numpy.ndenumerate(idct_array):
        (x, y) = x_y_idx
        idct = 0
        for u_v_idx, u_v in numpy.ndenumerate(array):
            (u, v) = u_v_idx
            idct += alphas_table[u, v] * u_v * cosines_table[x, u] * cosines_table[y, v]
        idct_array[x, y] = (round(idct) + centering_factor) % (2 * centering_factor) # cliping mod 256
    return idct_array

def fill_x_borders(expanded_array, x_start, last_y):
    expanded_array[x_start:, :] = expanded_array[x_start, last_y] 
    return

def fill_y_borders(expanded_array, y_start, last_x):
    array[:, y_start:] = expanded_array[last_x, y_start]
    return

print ('********************************************************************************')
print ('* Basic JPEG implementation                                                    *')
print ('********************************************************************************')
img_array = [[]]
expanded_array = [[]]
quantized_array = [[]]
dct_array = [[]]
dequantized_array = [[]]
idct_array = [[]]
error_array = [[]]

import sys
sys.path.append('../utils')
import userinput
fpath = userinput.get_img_path()
img_array = userinput.get_gray_img(fpath)
(img_array_x_len, img_array_y_len) = img_array.shape
#    
#img_array = zeros((8, 8))
#img_array[:, :] = [[52, 55, 61, 66, 70, 61, 64, 73],
#[63, 59, 55, 90, 109, 85, 69, 72],
#[62, 59, 68, 113, 144, 104, 66, 73],
#[63, 58, 71, 122, 154, 106, 70, 69],
#[67, 61, 68, 104, 126, 88, 68, 70],
#[79, 65, 60, 70, 77, 68, 58, 75],
#[85, 71, 64, 59, 55, 61, 65, 83],
#[87, 79, 69, 68, 65, 76, 78, 94]]
#(img_array_x_len, img_array_y_len) = (8, 8)

# do we need to fill the borders?!
x_mod = (img_array_x_len % 8)
y_mod = (img_array_y_len % 8)
expanded_x_len = (img_array_x_len + 8 - x_mod) if x_mod > 0 else img_array_x_len   
expanded_y_len = (img_array_y_len + 8 - y_mod) if y_mod > 0 else img_array_y_len   

# copy, resize and fill up array...
expanded_array = img_array.copy()
if (x_mod > 0) or (y_mod > 0):
    print 'expanding array to ' + (expanded_x_len, expanded_y_len) + '...'
    expanded_array.resize((expanded_x_len, expanded_y_len))
    if (expanded_x_len > img_array_x_len):
        fill_x_borders(quantized_array, img_array_x_len, img_array_y_len)
    if (expanded_y_len > img_array_y_len):
        fill_y_borders(quantized_array, img_array_y_len, expanded_y_len)

# initialize empty arrays...
quantized_array = zeros(img_array.shape)
dct_array = zeros(img_array.shape)
dequantized_array = zeros(img_array.shape)
idct_array = zeros(img_array.shape)

x_block_count = expanded_x_len / 8
y_block_count = expanded_y_len / 8
intensities = [1, 2, 4, 8, 16, 32];
for intensity in intensities: 
    
    print '\trunning JPEG (quantization matrix scale * %i)...' % (intensity)

    for x_block in range(0, x_block_count):
        for y_block in range(0, y_block_count):
            x_start, y_start = x_block * 8, y_block * 8 
            x_end, y_end = x_start + 8, y_start + 8
            # perform DCT and quantization over each 8x8 block
            dct_array[x_start:x_end, y_start:y_end] = dct(expanded_array[x_start:x_end, y_start:y_end].copy())
            quantized_array[x_start:x_end, y_start:y_end] = round(dct_array[x_start:x_end, y_start:y_end] / (quantization_array * intensity))
            # perform dequantization and inverse DCT over each 8x8 block
            dequantized_array[x_start:x_end, y_start:y_end] = quantized_array[x_start:x_end, y_start:y_end] * quantization_array * intensity
            idct_array[x_start:x_end, y_start:y_end] = idct(dequantized_array[x_start:x_end, y_start:y_end])

    # get the error rate
    error_rate = 0.
    error_array = img_array - idct_array
    for index, err in numpy.ndenumerate(error_array):
        error_rate += abs(err) 
    error_rate *= (1.0 / (64.0 * x_block_count * y_block_count))
    print '\t> error_rate: ', error_rate

    new_path = fpath + '.my_jpeg-' + str(intensity) + '.bmp'
    print '\t\tsaving image as \'%s\'' % (new_path)
    imsave(new_path, idct_array.astype('uint8'))

print ('********************************************************************************')