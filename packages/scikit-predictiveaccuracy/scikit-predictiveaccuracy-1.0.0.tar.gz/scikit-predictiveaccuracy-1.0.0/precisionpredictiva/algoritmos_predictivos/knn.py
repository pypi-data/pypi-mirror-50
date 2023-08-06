from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import numpy as np
from six import iteritems
import heapq

from .predicciones import PrediccionImposible
from .algo_base import AlgoBase


class AlgoritmoSimetrico(AlgoBase):

	def __init__(self, opciones_similitud = {}, verbose = True, **kwargs):

		AlgoBase.__init__(self, opciones_similitud = opciones_similitud, **kwargs)
		self.verbose = verbose


	def ajustar_modelo(self, entradas_entrenamiento):

		AlgoBase.ajustar_modelo(self,entradas_entrenamiento)

		bu = self.opciones_similitud['basado_usuario']
		self.n_x = self.conjunto_entrenamiento.n_usuarios if bu else self.conjunto_entrenamiento.n_peliculas
		self.n_y = self.conjunto_entrenamiento.n_peliculas if bu else self.conjunto_entrenamiento.n_usuarios
		self.xr = self.conjunto_entrenamiento.cu if bu else self.conjunto_entrenamiento.cp
		self.yr = self.conjunto_entrenamiento.cp if bu else self.conjunto_entrenamiento.cu

		return self

	def intercambiar(self, usuario, pelicula):

		if self.opciones_similitud['basado_usuario']:
			return usuario, pelicula
		else:
			return pelicula, usuario




class KNNPredictorBase(AlgoritmoSimetrico):


	def __init__(self, k = 50, min_k = 2, opciones_similitud = {}, parametros_bsl={}, verbose = True, **kwargs):

		AlgoritmoSimetrico.__init__(self, opciones_similitud = opciones_similitud, parametros_bsl=parametros_bsl,verbose=verbose ,**kwargs)

		self.k = k
		self.min_k = min_k

	def ajustar_modelo(self, entradas_entrenamiento):

		AlgoritmoSimetrico.ajustar_modelo(self,entradas_entrenamiento)
		self.b_u, self.b_i = self.calcular_sesgos(verbose=self.verbose)
		self.bx, self.by = self.intercambiar(self.b_u,self.b_i)
		self.sim = self.calcular_similitudes(verbose = self.verbose)

		return  self


	def estimar(self, usuario, pelicula):

		# PREDICTOR BASE 
		r_hat = self.conjunto_entrenamiento.promedio_global

		if self.conjunto_entrenamiento.existe_usuario(usuario):
			r_hat += self.b_u[usuario]
		
		if self.conjunto_entrenamiento.existe_pelicula(pelicula):
			r_hat += self.b_i[pelicula]

		# KNN 
		x,y = self.intercambiar(usuario,pelicula)

		if not (self.conjunto_entrenamiento.existe_usuario(usuario) and self.conjunto_entrenamiento.existe_pelicula(pelicula)):
			return r_hat

		vecinos = [(x2, self.sim[x, x2], r) for (x2, r) in self.yr[y]]
		k_vecinos = heapq.nlargest(self.k, vecinos, key=lambda t: t[1])


		# Calculo el promedio ponderado
		sum_sim = 0
		sum_cal = 0
		k_actual = 0

		for (nb,sim,c) in k_vecinos:
			if sim > 0:
				sum_sim += sim
				nb_bsl = self.conjunto_entrenamiento.promedio_global + self.bx[nb] + self.by[y]
				sum_cal += sim * (c - nb_bsl)
				k_actual += 1
		
		if k_actual < self.min_k:

			sum_cal = 0

		try:
			r_hat += sum_cal / sum_sim
		except ZeroDivisionError:
			pass


		detalles = {'k_actual':k_actual}
		return r_hat, detalles











