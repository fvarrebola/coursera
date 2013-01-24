from scipy import ndimage
import numpy
import pylab

print ('********************************************************************************')
print ('* Building a histogram using SciPy, NumPy and Pylab                            *')
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

# builds the histogram using ndimage.histogram()...
print ('\tbuilding histogram...')
bins_count = 256
histogram = ndimage.histogram(img_array, 0, 255, bins_count)

# plots the histogram using pylab...
print ('\tploting histogram...')
x_label = 'pixel'
y_label = 'number of pixels'
pylab.plot(histogram)
pylab.axis(xmax=bins_count)
pylab.axes().set_xlabel(x_label)
pylab.axes().set_ylabel(y_label)

hpath = fpath + '-histogram.png'
print ('\tsaving histogram to file \'' + hpath + '\'...')
pylab.savefig(fpath + '-histogram.png', format='png')

print ('\tshowing histogram...')
pylab.show()

print ('********************************************************************************')
