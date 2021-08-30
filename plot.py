import numpy
import matplotlib.pyplot as plt
import numpy, scipy
import matplotlib

thick = numpy.load('thick.npy')
bio = numpy.load('bio.npy')


fig=plt.figure()
one=fig.add_subplot(311)
one.plot(thick)

two=fig.add_subplot(312)
two.plot(bio)

fig.savefig("timeseries.pdf",format="pdf")
