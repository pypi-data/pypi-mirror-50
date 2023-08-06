from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from six.moves.urllib.request import urlretrieve
import zipfile
from collections import namedtuple
import os
from os.path import join



def obtener_directorio_dataset():

	carpeta = os.environ.get('CARPETA_MARCOS_DATA', os.path.expanduser('~') +'/.marcos_data/')

	if not os.path.exists(carpeta):
		os.makedirs(carpeta)

	return carpeta


DatasetIncorporado = namedtuple('DatasetIncorporado', ['url', 'path', 'escala_calificacion','reader_params'])

DATASETS_INCORPORADOS = { 
            'ml-latest-small':
                 DatasetIncorporado(
            url='http://files.grouplens.org/datasets/movielens/ml-latest-small.zip',
            path=join(obtener_directorio_dataset(), 'ml-latest-small/ml-latest-small/ratings.csv'),
            escala_calificacion = (1, 5),
            reader_params=dict(line_format='user item rating timestamp',sep=',')
        ),  
			'ml-100k':
        	DatasetIncorporado(
            url='http://files.grouplens.org/datasets/movielens/ml-100k.zip',
            path=join(obtener_directorio_dataset(), 'ml-100k/ml-100k/u.data'),
            escala_calificacion = (1, 5),
            reader_params=dict(line_format='user item rating timestamp',sep='\t')
        ),
    		'ml-1m':
       			 DatasetIncorporado(
            url='http://files.grouplens.org/datasets/movielens/ml-1m.zip',
            path=join(obtener_directorio_dataset(), 'ml-1m/ml-1m/ratings.dat'),
            escala_calificacion = (1, 5),
            reader_params=dict(line_format='user item rating timestamp',sep='::')
        )

}


def descargar_datasets(nombre):
    dataset = DATASETS_INCORPORADOS[nombre]

    print("Intentando descargar el conjunto de datos desde " + dataset.url + '...')
	
    directorio_archivo_temporal = join(obtener_directorio_dataset(),'tmp.zip')
    urlretrieve(dataset.url, directorio_archivo_temporal)

    with zipfile.ZipFile(directorio_archivo_temporal,'r') as zip_temporal:
        zip_temporal.extractall(join(obtener_directorio_dataset(),nombre))
    os.remove(directorio_archivo_temporal)
    print("El dataset", nombre, ' ha sido guardado en ',join(obtener_directorio_dataset(),nombre))






