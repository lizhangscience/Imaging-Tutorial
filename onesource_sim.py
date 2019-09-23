import numpy
from scipy import constants
import re

os.system('rm -rf Point_source.cl')
cl.done()
cl.addcomponent(dir="J2000 0h0m0s 0d0m0s", flux=2, fluxunit='Jy',freq="4.0 GHz", spectrumtype="Constant", shape="point")
cl.rename('Point_source.cl')
cl.done()

simobserve(project = 'point_source_onesource',
    complist = 'Point_source.cl',
    direction = "J2000 0h0m0s 0d0m0s",
    obsmode = 'int',
    antennalist = 'vla.a.cfg',
    totaltime = '1s',
    thermalnoise = '')

os.chdir('point_source_onesource/')

miu = 4.0e+09
wavelength = constants.c/miu
numpy.set_printoptions(threshold='nan') #This prevents numpy truncating the print out of large arrays.
tb.open('point_source_onesource.vla.a.ms', nomodify=F) #Opens your Measurement Set
uvw = tb.getcol('UVW') #Puts UVW data information into array uvw.
uvw = uvw.transpose() #transposes uvw array into uvw_col such that there are 3 columns representing u v and w values.
uvw = uvw/wavelength # so that u v and w are in wavelength
mydata = tb.getcol('DATA') #Puts visibility data information into array mydata.
data = mydata[0].transpose()
wt = numpy.ones([351,1]) #weights, I chose 1 for every visibility
output = numpy.concatenate((uvw,data.real,data.imag,wt),axis=1)
numpy.savetxt('onesource.csv',output) # saves uvw_col to a text file named 'namefile'.
tb.close()#Closes your Measurement Set

#make a dirty map
clean(vis = 'point_source_onesource.vla.a.ms',
    imagename = 'point_source_onesource.dirty',
    imsize = 200,
    cell = 0.05,
    niter = 0,
    usescratch = F,
    weighting = 'natural')
