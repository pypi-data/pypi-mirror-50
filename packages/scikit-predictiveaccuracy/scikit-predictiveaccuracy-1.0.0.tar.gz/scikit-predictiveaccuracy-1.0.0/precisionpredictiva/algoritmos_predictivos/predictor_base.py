

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .algo_base import AlgoBase

class PredictorBase(AlgoBase):

	def __init__(self, parametros_bsl= {}, verbose = True):

		AlgoBase.__init__(self, parametros_bsl = parametros_bsl)
		self.verbose = verbose


	def ajustar_modelo(self, entradas_entrenamiento):


		AlgoBase.ajustar_modelo(self,entradas_entrenamiento)

		# Llamo a la funcion calcular_sesgos()
		self.b_u, self.b_i = self.calcular_sesgos(self.verbose)

		# Devuelvo el objeto, ajustado.
		return self


	def estimar(self, usuario, pelicula):
		
		# Promedio global
		r_hat = self.conjunto_entrenamiento.promedio_global

		# Sesgo usuario
		if self.conjunto_entrenamiento.existe_usuario(usuario):
			r_hat += self.b_u[usuario]
		# Sesgo pellicula
		if self.conjunto_entrenamiento.existe_pelicula(pelicula):
			r_hat += self.b_i[pelicula]
			
		#Devuelvo calificacion predicha
		return r_hat 

