
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
cimport numpy as np
import numpy as np
from six.moves import range

def sgd_sesgos(self):

	cdef np.ndarray[np.double_t] b_u = np.zeros(self.conjunto_entrenamiento.n_usuarios)
	cdef np.ndarray[np.double_t] b_i = np.zeros(self.conjunto_entrenamiento.n_peliculas)
	
	cdef int usuario, pelicula 
	cdef double calificacion, error
	cdef double promedio_global = self.conjunto_entrenamiento.promedio_global	

	cdef int n_epocas = self.parametros_bsl.get('n_epocas', 20)
	cdef double tasa_reg = self.parametros_bsl.get('tasa_regularizacion', 0.02)
	cdef double tasa_apren = self.parametros_bsl.get('tasa_aprendizaje', 0.003)

	for _ in range(n_epocas):
		for usuario, pelicula, calificacion in self.conjunto_entrenamiento.todas_calificaciones():
			error = (calificacion - (promedio_global + b_u[usuario] + b_i[pelicula]))
			b_u[usuario] += tasa_apren * (error - tasa_reg * b_u[usuario])
			b_i[pelicula] += tasa_apren * (error - tasa_reg * b_i[pelicula])

	return b_u, b_i








