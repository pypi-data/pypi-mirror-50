from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import time
import numpy as np
from joblib import Parallel
from joblib import delayed
from six import iteritems
from numba import jit

from .split import obtener_cv
from .. import precision



def validacion_cruzada(algoritmo, 
						data, 
						metricas = ['rmse'], 
						folds = None, 
						rmse_entrenamiento = False, 
						n_jobs= 1, 
						pre_dispatch ='2*n_jobs', 
						verbose = False):


	metricas = [m.lower() for m in metricas]
	vc = obtener_cv(folds)
	# Comprension de tuplas
	lista_re = (delayed(ajustar_y_evaluar)(algoritmo, entradas_entrenamiento, entradas_prueba, metricas,rmse_entrenamiento)	for (entradas_entrenamiento,entradas_prueba) in vc.split(data))	

	# Proceso en paralelo (igual, no es muy rápido :)
	salida = Parallel(n_jobs= n_jobs, pre_dispatch=pre_dispatch)(lista_re)


	(dicccionario_metrica_prueba, 
	diccionario_metrica_entrenamiento,
	tiempo_ajuste, 
	tiempo_prueba) = zip(*salida)

	metrica_prueba = dict()
	metrica_entrenamiento = dict()
	devolver = dict()

	for m in metricas:
		metrica_prueba[m] =  np.asarray( [d[m] for d in dicccionario_metrica_prueba] )
		devolver[ m + '_prueba'] = metrica_prueba[m]
		if rmse_entrenamiento:
			metrica_entrenamiento[m] = np.asarray([ d[m] for d in diccionario_metrica_entrenamiento])
			devolver[m+ '_entrnamiento'] = metrica_entrenamiento[m]


	devolver['tiempo_ajuste'] = tiempo_ajuste
	devolver['tiempo_prueba'] = tiempo_prueba

	if verbose == True:
		imprimir_resumen(algoritmo, metricas, metrica_prueba, metrica_entrenamiento, tiempo_ajuste, tiempo_prueba,vc.n_particiones)

	return devolver



def ajustar_y_evaluar(algoritmo, entradas_entrenamiento, entradas_prueba, metricas, rmse_entrenamiento=False):


	inicio_ajuste = time.time()
	algoritmo.ajustar_modelo(entradas_entrenamiento)
	tiempo_ajuste = time.time() - inicio_ajuste

	inicio_prueba = time.time()
	predicciones = algoritmo.prueba(entradas_prueba)
	tiempo_prueba = time.time() - inicio_prueba

	if rmse_entrenamiento:
		predicciones_entrenamiento = algoritmo.prueba(entradas_entrenamiento.construir_entradasprueba())

	metrica_prueba = dict()
	metrica_entrenamiento = dict()

	for m in metricas:
		 j = getattr(precision, m.lower())
		 metrica_prueba[m] = j(predicciones, verbose = 0)
		 if rmse_entrenamiento:
		 	metrica_entrenamiento[m] = j(predicciones_entrenamiento, verbose = 0)

	return metrica_prueba, metrica_entrenamiento, tiempo_ajuste, tiempo_prueba



def imprimir_resumen(algoritmo, 
					  metricas, 
					  metricas_prueba, 
					  metrica_entrenamiento, 
					  tiempos_ajuste, 
					  tiempos_prueba, 
					  n_particiones):
	
	print('\nEvaluando {0} del algoritmo {1} sobre {2} particiones.'.format(
          ', '.join((m.upper() for m in metricas)),
          algoritmo.__class__.__name__, n_particiones))
	print()


	formato_fila = '{:<18}' + '{:<8}' * (n_particiones + 2)
	u = formato_fila.format(
        '',
        *['Fold {0}'.format(i + 1) for i in range(n_particiones)] + ['Prom'] + ['Std'])
	u += '\n'
	u += '\n'.join(formato_fila.format(key.upper() + 
		' (validación)',*['{:1.4f}'.format(v) for v in vals] +
		['{:1.4f}'.format(np.mean(vals))] + 
		['{:1.4f}'.format(np.std(vals))]) 
	for (key, vals) in iteritems(metricas_prueba))


		
	if metrica_entrenamiento:
		u += '\n'
		u += '\n'.join(formato_fila.format(key.upper() +
		 ' (entrenamie)',    
		 *['{:1.4f}'.format(v) for v in vals] + 
		 ['{:1.4f}'.format(np.mean(vals))] + 
		 ['{:1.4f}'.format(np.std(vals))]) for (key, vals) in iteritems(metrica_entrenamiento))


	u += '\n'
	u += formato_fila.format('Tiempo de ajuste:',
                           *['{:.2f}'.format(t) for t in tiempos_ajuste] +
                           ['{:.2f}'.format(np.mean(tiempos_ajuste))] +
                           ['{:.2f}'.format(np.std(tiempos_ajuste))])

	u += '\n'
	u += formato_fila.format('Tiempo de prueba:',
                           *['{:.2f}'.format(t) for t in tiempos_prueba] +
                           ['{:.2f}'.format(np.mean(tiempos_prueba))] +
                           ['{:.2f}'.format(np.std(tiempos_prueba))])
	print(u)















































