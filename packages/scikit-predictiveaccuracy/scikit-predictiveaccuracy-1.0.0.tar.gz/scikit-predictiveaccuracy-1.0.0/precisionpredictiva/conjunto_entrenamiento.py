	
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np
from six import iteritems



class ConjuntoEntrenamiento:

	def __init__(self, calificacion_usuario, calificacion_pelicula,	cant_usuarios, cant_peliculas,cant_calificaciones, escala_calificacion, raw2inner_id_usuarios, raw2inner_id_peliculas ):


		self.cu = calificacion_usuario
		self.cp = calificacion_pelicula
		self.n_usuarios = cant_usuarios
		self.n_peliculas = cant_peliculas
		self.n_calificaciones = cant_calificaciones
		self.escala_calificacion = escala_calificacion
		self._raw2inner_id_usuarios = raw2inner_id_usuarios
		self._raw2inner_id_peliculas = raw2inner_id_peliculas
		self._promedio_global = None
		self._inner2raw_id_usuarios = None
		self._inner2raw_id_peliculas = None

	

	def existe_usuario(self, idu):
		return idu in self.cu


	def existe_pelicula(self,idp):
		return idp in self.cp


	def to_inner_uid(self, ruid):
		
		try:
			return self._raw2inner_id_usuarios[ruid]
		
		except KeyError:
			raise ValueError('El usuario ' +str(ruid)+' no es parte de las entradas de entrenamiento')


	def to_raw_uid(self, iuid):

		if self._inner2raw_id_usuarios is None:
			self._inner2raw_id_usuarios = {inner: raw for (raw, inner) in iteritems(self._raw2inner_id_usuarios)}

		try:
			return self._inner2raw_id_usuarios[iuid]
		except KeyError:
			raise ValueError(str(iuid)+ ' no es un inner id valido')

	def to_inner_iid(self,riid):
		try:
			return self._raw2inner_id_peliculas[riid]
		except KeyError:
			raise ValueError('La pelicula ' +str(riid)+' no es parte de las entradas de entrenamiento')


	def to_raw_iid(self,iiid):

		if self._inner2raw_id_peliculas is None:
			self._inner2raw_id_peliculas = { inner: raw for (raw, inner) in iteritems(self._raw2inner_id_peliculas)}

		try:
			return self._inner2raw_id_peliculas[iiid]

		except KeyError:
			raise  ValueError( str(iiid) +' no es un inner id valido')


	# Funcion para iterar sobre todas las califiaciones
	def todas_calificaciones(self):

		for u, c_usuario in iteritems(self.cu):
			for pelicula, calificacion in c_usuario:
				yield u, pelicula, calificacion

	
	def construir_entradasprueba(self):
		return [(self.to_raw_uid(usuario), self.to_raw_iid(pelicula), calificacion)
                for (usuario, pelicula, calificacion) in self.todas_calificaciones()]


	def iterarador_usuarios(self):
		return range(self.n_usuarios)
	
	def iterador_peliculas(self):
		return range(self.n_peliculas)

	@property
	def promedio_global(self):
		if self._promedio_global is None:
			self._promedio_global = np.mean([c for (_,_,c) in self.todas_calificaciones()])

		return self._promedio_global



































