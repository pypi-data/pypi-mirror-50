from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from collections import defaultdict
import numpy as np
from six import iteritems



def rmse(predicciones, verbose = True):

	if not predicciones:
		raise  ValueError('La lista de predicciones está vacía.')

	mse = np.mean([float(c_verdadera - c_estimada)**2 for (_,_,c_verdadera,c_estimada,_) in predicciones])

	rmse_ = np.sqrt(mse)

	if verbose:
		print("Se obtuvo un RMSE de {0:1.4f}".format(rmse_))

	return rmse_