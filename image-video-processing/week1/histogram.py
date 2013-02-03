from scipy import ndimage
import numpy
import pylab

print ('********************************************************************************')
print ('* Building a histogram using SciPy, NumPy and Pylab                            *')
print ('********************************************************************************')
import sys
sys.path.append('../utils')
import userinput
fpath = userinput.get_img_path()
img_array = userinput.get_gray_img(fpath)


# builds the histogram using ndimage.histogram()...
print ('building histogram...')
bins_count = 256
histogram = ndimage.histogram(img_array, 0, 255, bins_count)

# plots the histogram using pylab...
print ('ploting histogram...')
x_label = 'pixel'
y_label = 'number of pixels'
pylab.plot(histogram)
pylab.axis(xmax=bins_count)
pylab.axes().set_xlabel(x_label)
pylab.axes().set_ylabel(y_label)

hpath = fpath + '-histogram.png'
print ('saving histogram to file \'' + hpath + '\'...')
pylab.savefig(fpath + '-histogram.png', format='png')

print ('showing histogram...')
pylab.show()

print ('********************************************************************************')