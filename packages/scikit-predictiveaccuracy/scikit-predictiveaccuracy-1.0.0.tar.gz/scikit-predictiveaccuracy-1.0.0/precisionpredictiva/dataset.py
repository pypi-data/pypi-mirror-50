from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from collections import defaultdict
import sys
import os
import itertools
import random
import warnings

from six.moves import input
from six.moves import range

from .reader import Reader
from .datasets_incorporados import descargar_datasets
from .datasets_incorporados import DATASETS_INCORPORADOS
from .conjunto_entrenamiento import ConjuntoEntrenamiento



class Dataset:

	

	def __init__(self, reader=None, escala_calificacion=None):

		self.reader = reader
		self.escala_calificacion = escala_calificacion

		if self.escala_calificacion is None:
			raise ValueError("Eppaaaa")
			warnings.warn("Usando la escala de califiacion de la clase Reader")
		self.escala_calificacion = self.reader.escala_cali



	@classmethod
	def cargar_incorporado(cls,	nombre='ml-100k', prompt=True):

		try:
			dataset = DATASETS_INCORPORADOS[nombre]
		except KeyError:
			raise  ValueError('Dataset desconocido. Vuelve a intentarlo!')

		# Si el dataset no existe, lo bajamos

		if not os.path.isfile(dataset.path):
			respondido = not prompt
			while not respondido:
				print("Dataset " +nombre+ " no se encontró en el sistema. Lo queres descargar? [Si/no] ",end='')
				eleccion = input().lower()

				if eleccion in ['Si','s','si']:
					respondido = True
				elif eleccion in ['No','n','no']:
					respondido = True
					print("Okay, nos vemos en otro momento!")
					sys.exit()

			descargar_datasets(nombre)

		reader = Reader(**dataset.reader_params)
		
		return cls.cargar_desde_archivo(ruta_archivo = dataset.path, reader=reader, escala_calificacion=dataset.escala_calificacion)


	
	@classmethod
	def cargar_desde_archivo(cls, ruta_archivo, reader, escala_calificacion=None):
		return DatasetAutoParticion(archivo_calificaciones=ruta_archivo,reader=reader,escala_calificacion=escala_calificacion)


	
	def leer_calificaciones(self,nombre_archivo):
		with open(os.path.expanduser(nombre_archivo)) as f:
			raw_ratings = [ self.reader.leer_linea(linea) for linea in itertools.islice(f, self.reader.saltar_lineas, None)]
		return raw_ratings



	def crear_conjunto_entrenamiento(self, conjunto_crudo):
		
		raw2inner_id_usuarios = {}
		raw2inner_id_peliculas = {}


		indice_actual_usuario = 0
		indice_actual_pelicula = 0

		calificacion_usuario = defaultdict(list)
		calificacion_pelicula = defaultdict(list)

		
		# user raw id, item raw id, translated rating, time stamp
		for urid, irid, c, timestamp in conjunto_crudo:
			

			try:
				uid = raw2inner_id_usuarios[urid]
			except KeyError:
				uid  = indice_actual_usuario
				raw2inner_id_usuarios[urid] = indice_actual_usuario
				indice_actual_usuario += 1
			

			try:
				iid = raw2inner_id_peliculas[irid]
			
			except KeyError:
				iid = indice_actual_pelicula
				raw2inner_id_peliculas[irid] = indice_actual_pelicula
				indice_actual_pelicula += 1


			calificacion_usuario[uid].append((iid,c))
			calificacion_pelicula[iid].append((uid,c))

		n_usuarios = len(calificacion_usuario)
		n_peliculas = len(calificacion_pelicula)
		n_calificaciones = len(conjunto_crudo)

		conjunto_entrenamiento = ConjuntoEntrenamiento( calificacion_usuario,
														calificacion_pelicula,
														n_usuarios,
														n_peliculas,
														n_calificaciones,
														self.escala_calificacion,
														raw2inner_id_usuarios,
														raw2inner_id_peliculas)
		return conjunto_entrenamiento

	

	def crear_conjunto_prueba(self, conjunto_crudo_prueba):
		
		return [ (ruid, riid, r_ui_trans) for (ruid, riid, r_ui_trans,_) in conjunto_crudo_prueba]




class DatasetAutoParticion(Dataset):

	


	def __init__(self, archivo_calificaciones=None,reader=None,df=None, escala_calificacion=None):


		Dataset.__init__(self, reader, escala_calificacion)

		self.ha_sido_dividido = False # Centinela

		if archivo_calificaciones is not None:
			self.archivo_calificaciones = archivo_calificaciones
			self.raw_ratings = self.leer_calificaciones(self.archivo_calificaciones)
		
		# Si se me antoja un Dataframe
		elif df is not None:
			self.df = df
			self.raw_ratings = [(uid, iid, float(r), None) for (uid, iid, r) in self.df.itertuples(index=False)]
		else:
			raise ValueError('Tenés que especificar el archivo de califiaciones o dataframe')




	def construir_conjuntoentrenamiento_completo(self):
		return self.crear_conjunto_entrenamiento(self.raw_ratings)

	


	def particion_cruda(self):

		if not self.ha_sido_dividido:
			self.split()


			def k_folds(seq,n_particiones):
				iniciar, parar = 0,0 
				for particion_i in range(n_particiones):
					iniciar = parar
					fin += len(seq) // n_particiones
					if particion_i < len(seq) % n_particiones:
						parar +=1
					yield seq[:iniciar] + seq[parar:], seq[iniciar:parar]
		return k_folds(self.raw_ratings, self.n_particiones)

	

	def split(self, n_particiones=5, mezclar=True):
		if n_particiones > len(raw_ratings) or n_particiones < 2:
			raise ValueError("Valor incorrecto para la cantidad de particiones. Debe ser mayor o igual a 2")
		if mezclar:
			random.shuffle(self.raw_ratings)
		
		self.n_particiones  = n_particiones
		self.ha_sido_dividido = True

























