import math
import numpy as np

def Berfun(x):
	"""
	Compute the Bernouli's function.
	Its definition is
	Bexfun(x)=x/(exp(x)-1)
	"""
	ber = np.ones(x.shape)
	ind1 = np.where(x>1e-10)
	ind2 = np.where(x<-1e-10)
	exp1 = np.exp(-x[ind1])
	ber[ind1] = x[ind1]*exp1/(1.-exp1)
	ber[ind2] = x[ind2]/(np.exp(x[ind2])-1.)

	bern = x+ber
	return ber,bern
