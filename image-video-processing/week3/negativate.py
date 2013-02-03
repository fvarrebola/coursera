from scipy.misc.pilutil import imsave
import numpy
import sys

print ('********************************************************************************')
print ('* Really simple negative image                                                 *')
print ('********************************************************************************')
sys.path.append('../utils')
import userinput
fpath = userinput.get_img_path()
img_array = userinput.get_gray_img(fpath)
(img_array_x_len, img_array_y_len) = img_array.shape
new_img_array = 255 - img_array
new_path = fpath + '.grayscale-negative.bmp'
print 'saving grayscale negative image as \'%s\'...' % (new_path)
imsave(new_path, new_img_array)
print ('********************************************************************************')
