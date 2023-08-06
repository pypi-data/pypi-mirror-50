


from __future__ import (absolute_import, division, print_function, unicode_literals)
from itertools import chain
from math import ceil, floor
import numbers
from collections import defaultdict
from six import iteritems
from six import string_types
import numpy as np


from ..utilidades import generador_aleatorio


def obtener_cv(folds):
	
	if folds is None:
		return Kfold(n_particiones = 5)

	if isinstance(folds,numbers.Integral):
		return Kfold(n_particiones = folds)


	# The hasattr() method returns true if an object has the given named attribute and false if it does not.
	if hasattr(folds,'split') and not isinstance(folds,string_types):
		return folds 



class Kfold():

	def __init__(self, n_particiones=5, random_state=None, mezclar=True):
		
		self.n_particiones = n_particiones
		self.mezclar = mezclar
		self.random_state = random_state


	def split(self, data):

		if self.n_particiones > len(data.raw_ratings) or self.n_particiones < 2:

			raise ValueError('Valor incorrecto para n_particiones = {0}. '
				'Tiene que ser mayor o igual a dos '
				'y menor que la cantidad de califiaciones'.format(self.n_particiones))

		indices = np.arange(len(data.raw_ratings))


		if self.mezclar:
			generador_aleatorio(self.random_state).shuffle(indices)


		iniciar, detener = 0, 0

		for particion_i in range(self.n_particiones):
			iniciar = detener 
			detener += len(indices) // self.n_particiones
			if particion_i < len(indices) % self.n_particiones:
				detener += 1

			raw_trainset = [data.raw_ratings[i] for i in chain(indices[:iniciar],
                                                               indices[detener:])]

			raw_testset = [data.raw_ratings[i] for i in indices[iniciar:detener]]

			conjunto_entrenamiento = data.crear_conjunto_entrenamiento(raw_trainset)
			conjunto_prueba = data.crear_conjunto_prueba(raw_testset)

			yield conjunto_entrenamiento, conjunto_prueba

	def obtener_n_folds(self):
		return self.n_particiones



class BarajarDividir():

	
	def __init__(self, n_particiones = 5, 
					   tamano_prueba = .2, 
					   tamano_entrenamiento =None, 
					   random_state=None, 
					   mezclar= True):

		
		if n_particiones <= 0:
			raise ValueError("n_particiones = {0} tiene que ser estrictamente mayor que " '0'.format(n_particiones))

		
		if tamano_prueba is not None and tamano_prueba <= 0:
			raise ValueError('tamano_prueba = {0} tiene que estrictamente mayor que ' '0'.format(tamano_prueba))


		if tamano_entrenamiento is not None and tamano_entrenamiento <= 0:
			raise ValueError('tamano_entrenamiento{0} tiene que ser estrictamente mayor que ' '0'.format(tamano_entrenamiento))

		self.n_particiones = n_particiones
		self.tamano_prueba = tamano_prueba
		self.tamano_entrenamiento = tamano_entrenamiento
		self.random_state = random_state
		self.mezclar = mezclar

	

	def validar_tamanos_entrenamiento_prueba(self, tamano_prueba, tamano_entrenamiento, cant_calificaciones):

		if tamano_prueba is not None and tamano_prueba >= cant_calificaciones:
			raise ValueError('tamano_prueba={0} debe ser menor que la cantidad de ' ' calificaciones{1}'.format(tamano_prueba,cant_calificaciones))

		if tamano_entrenamiento is not None and tamano_entrenamiento >= cant_calificaciones:
			raise ValueError('tamano_entrenamiento={0} debe ser menor que la cantidad de ' ' calificaciones{1}'.format(tamano_entrenamiento,cant_calificaciones))

		if np.asarray(tamano_prueba).dtype.kind == 'f':
			# El método ceil () devuelve el valor de techo de x, es decir, el entero más pequeño, no menor que x.
			tamano_prueba = ceil(tamano_prueba * cant_calificaciones)


		if tamano_entrenamiento is None:
			tamano_entrenamiento = cant_calificaciones - tamano_prueba
		elif np.asarray(tamano_entrenamiento).dtype.kind == 'f':
			tamano_entrenamiento = floor(tamano_entrenamiento * cant_calificaciones)

		if tamano_prueba is None:
			tamano_prueba = cant_calificaciones - tamano_entrenamiento


		if tamano_entrenamiento + tamano_prueba > cant_calificaciones:
			raise ValueError("La suma entre el tamaño de entrenamiento y el de prueba ({0})"'deberia ser menor que el numero de ''califiaciones {1}'.format(tamagno_prueba + tamano_entrenamiento, cant_calificaciones))


		return int(tamano_entrenamiento), int(tamano_prueba)

	

	def split(self,data):


		tamano_prueba, tamano_entrenamiento = self.validar_tamanos_entrenamiento_prueba(self.tamano_prueba,self.tamano_entrenamiento, len(data.raw_ratings))
		ga = generador_aleatorio(self.random_state)

		for _ in range(self.n_particiones):

			if self.mezclar:
				permutacion = ga.permutation(len(data.raw_ratings))

			else:
				permutacion = np.arange(len(data.raw_ratings))

			raw_trainset = [data.raw_ratings[i] for i in permutacion[:tamano_prueba]]

			raw_testset = [data.raw_ratings[i] for i in permutacion[tamano_prueba:(tamano_prueba + tamano_entrenamiento)]]

			conjunto_entrenamiento = data.crear_conjunto_entrenamiento(raw_trainset)
			
			conjunto_prueba = data.crear_conjunto_prueba(raw_testset)

			yield conjunto_entrenamiento, conjunto_prueba



def division_entrenamiento_prueba(data, tamano_prueba = .2, tamano_entrenamiento=None, random_state=None, mezclar=True):

		# Instancio la clase
		bd = BarajarDividir(n_particiones =1,
							 tamano_prueba= tamano_prueba,
							 tamano_entrenamiento=tamano_entrenamiento, 
							 random_state=False, 
							 mezclar= mezclar)
		# The next() function returns the next item in an iterator.
		return next(bd.split(data))












































