import numpy
import matplotlib.pyplot as plt
import numpy, scipy
import matplotlib

thick = numpy.load('thick.npy')
bio = numpy.load('bio.npy')
grazing = numpy.load('slope.npy')


fig=plt.figure()
one=fig.add_subplot(311)
one.plot(thick)
one.set_ylabel("soil thickness")

two=fig.add_subplot(312)
two.plot(bio)
two.set_ylabel("biomass")

two=fig.add_subplot(313)
two.plot(grazing)
two.set_ylabel("grazing pressure")
two.set_xlabel("time (years)")

fig.savefig("timeseries.pdf",format="pdf")
