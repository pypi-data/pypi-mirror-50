
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import warnings

from six import get_unbound_function as guf


from .. import metricas_similitud as sims
from .predicciones import PrediccionImposible
from .predicciones import Prediccion
from .optimizador_sesgos import sgd_sesgos



class AlgoBase(object):
	
	# Constructor
	def __init__(self, **kwargs):
		
		self.parametros_bsl = kwargs.get('parametros_bsl',{})
		self.opciones_similitud = kwargs.get('opciones_similitud',{})

		if 'basado_usuario' not in self.opciones_similitud:
			self.opciones_similitud['basado_usuario'] = True

		self.saltar_entrenamiento = False

		if (guf(self.__class__.ajustar_modelo) is guf(AlgoBase.ajustar_modelo) and guf(self.__class__.entrenar) is not guf(AlgoBase.entrenar)):
				warnings.warn('It looks like this algorithm (' +
                          str(self.__class__) +
                          ') implements train() '
                          'instead of fit(): train() is deprecated, '
                          'please use fit() instead.', UserWarning)

	
	def entrenar(self, entradas_entrenamiento):
		
		self.saltar_entrenamiento = True
		self.ajustar_modelo(entradas_entrenamiento)


		return self


	

	def ajustar_modelo(self, entradas_entrenamiento):

		if (guf(self.__class__.entrenar) is not guf(AlgoBase.entrenar) and not self.saltar_entrenamiento):

			self.entrenar(entradas_entrenamiento)

			return 
		
		self.saltar_entrenamiento = False

		self.conjunto_entrenamiento = entradas_entrenamiento

		# (Re) Inicializar sesgos
		self.b_u = self.b_i = None

		return self

	

	def predecir(self, idusuario, idpelicula, r_ui=None, cortar=True, verbose=False):

		try:
			iuid = self.conjunto_entrenamiento.to_inner_uid(idusuario)
		except ValueError:
			iuid  =  str(idusuario) + '__DESCONOCIDO' 

		try:
			iiid = self.conjunto_entrenamiento.to_inner_iid(idpelicula)
		except ValueError:
			iiid = str(idpelicula) + '__DESCONOCIDO'

		detalles = {}
		try:
			r_hat = self.estimar(iuid,iiid)

			if isinstance(r_hat, tuple):
				r_hat, detalles = r_hat

			detalles['imposible_calcular'] = False

		except PrediccionImposible as e:
			r_hat = self.prediccion_defecto()
			detalles['imposible_calcular'] = True
			detalles['razon'] = str(e)


		# Recorto la califiacion predicha para que esté en el rango [inferior,superior]

		if cortar:
			limite_inferior, limite_superior = self.conjunto_entrenamiento.escala_calificacion
			r_hat = min(limite_superior,r_hat)
			r_hat = max(limite_inferior,r_hat)


		pred = Prediccion(idusuario, idpelicula, r_ui, r_hat, detalles)

		if verbose:
			print(pred)

		return pred



	def prediccion_defecto(self):

		return  self.conjunto_entrenamiento.promedio_global


	

	def prueba(self, entradas_prueba, verbose=False):

		predicciones = [self.predecir(idusuario, idpelicula, r_ui_trans, verbose=verbose) for (idusuario, idpelicula, r_ui_trans) in entradas_prueba]

		return predicciones

	
	

	def calcular_sesgos(self,verbose=False):

		tecnica = dict(sgd=sgd_sesgos)
		nombre_tecnica = self.parametros_bsl.get('tecnica', 'sgd')
		
		try:
			if verbose:
				print("Obteniendo los sesgos b_{u} y b_{i} usando Descenso Estocástico de Gradiente...")
				self.b_u, self.b_i = tecnica[nombre_tecnica](self)
			return self.b_u, self.b_i
		except KeyError:
			raise ValueError("Tecnica errónea " +nombre_tecnica+ " para el calculo de los sesgos.")

	


	def calcular_similitudes(self, verbose = True):


		funcion_cons = {'coseno':sims.coseno,'pearson':sims.pearson,'pearson_baseline':sims.pearson_baseline}

		if self.opciones_similitud['basado_usuario']:
			n_x, yr = self.conjunto_entrenamiento.n_usuarios, self.conjunto_entrenamiento.cp

		else:
			n_x, yr = self.conjunto_entrenamiento.n_peliculas, self.conjunto_entrenamiento.cu

		soporte_min = self.opciones_similitud.get('min_support',1)

		args = [n_x, yr, soporte_min]
		
		nombre = self.opciones_similitud.get('nombre','pearson').lower()

		if nombre == 'pearson_baseline':
			shrinkage = self.opciones_similitud.get('shrinkage',100)
			b_u, b_i = self.calcular_sesgos()
			if self.opciones_similitud['basado_usuario']:
				bx, by = b_u, b_i
			else:
				bx, by = b_i, b_u

			args += [self.conjunto_entrenamiento.promedio_global, bx, by, shrinkage]

		try:
			if verbose:
				print("Calculando la matriz (D) de similitud usando {0}...".format(nombre.upper()))
			
			sim = funcion_cons[nombre](*args)
			
			if verbose:
				print("El cálculo de la matriz (D) de similitud ha finalizado.")

			return sim

		except KeyError:
			raise NameError('Nombre de metrica incorrecto.')


	

	def obtener_vecinos(self, iid, k):
		
		if self.opciones_similitud['basado_usuario']:
			todas_inst = self.conjunto_entrenamiento.iterador_usuarios
		else:
			todas_inst = self.conjunto_entrenamiento.iterador_peliculas

		otros = [(x, self.sim[iid,x]) for x in todas_inst() if x !=iid]
		k_vecinos_mas_cercanos = [l for (l,_) in otros[:k]]

		return k_vecinos_mas_cercanos

		













































































































