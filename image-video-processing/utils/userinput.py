from copy import copy
from numpy.core.numeric import zeros
from numpy.ma.core import cos, floor, sqrt, size
from numpy.numarray.functions import reshape, round
from scipy import ndimage
from scipy.constants.constants import pi
from scipy.misc.pilutil import imsave
import numpy

def rgb2gray(rgb):
    r, g, b = numpy.rollaxis(rgb[...,:3], axis = -1)
    return 0.299 * r + 0.587 * g + 0.114 * b

def get_img_path():
    fpath = raw_input('> image\'s full path:')
    try:
        with open(fpath) as f: pass
    except IOError as e:
        print (fpath + ' could not be opened')
        raise
    return fpath;

def get_gray_img(fpath):
    img_array = numpy.array(ndimage.imread(fpath));
    shape_len = len(img_array.shape)
    if (shape_len == 3):
        grayscale_img_array = rgb2gray(img_array);
    elif (shape_len == 2): 
        grayscale_img_array = img_array;
    else:
        raise Exception('unsupported image...')
    return grayscale_img_array;

def get_rgb_img():
    img_array = numpy.array(ndimage.imread(fpath));
    shape_len = len(img_array.shape)
    if (shape_len != 3):
        raise Exception('unsupported image...')
    return img_array;