
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


from .datasets_incorporados import DATASETS_INCORPORADOS 


class Reader():

	def __init__(self, nombre = None, line_format = 'user item rating', sep=None, escala_calificacion=(1,5), saltar_lineas=0):


		if nombre:
			try:
				self.__init__(**DATASETS_INCORPORADOS[nombre].reader_params)
			except KeyError:
				raise ValueError('Lector desconocido ' +nombre+ ' se aceptan valores como: 	'+','.join(DATASETS_INCORPORADOS.keys())+'.')

		else:
			self.sep = sep
			self.saltar_lineas = saltar_lineas
			self.escala_cali = escala_calificacion


			limite_inferior, limite_superior = escala_calificacion
			self.offset = -limite_inferior + 1 if limite_inferior <= 0 else 0

			formato_separado = line_format.split()

			entidades = ['user','item','rating']
			if 'timestamp' in formato_separado:
				self.con_marcatemporal = True
				entidades.append('timestamp')
			else:
				self.con_marcatemporal = False

			# Chequo que todos los campos esten okay
			if any(campo not in entidades for campo in formato_separado):
				raise  ValueError('El formato_linea es incorrecto.')

			self.indices = [formato_separado.index(entidad) for entidad in entidades]

	def leer_linea(self,linea):

		linea = linea.split(self.sep)

		try:
			if self.con_marcatemporal:

				idu, idp, c, marcatemporal = (linea[i].strip() for i in self.indices)

			else:
				idu, idp, c = (linea[i].strip() for i in self.indices)

		except IndexError:
			raise ValueError("No es posible leer la linea. Chequea el formato de linea y los separadores de linea")


		return idu, idp, float(c), marcatemporal







