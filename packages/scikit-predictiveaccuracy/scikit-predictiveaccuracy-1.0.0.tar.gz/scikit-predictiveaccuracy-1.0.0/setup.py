from setuptools import  find_packages, Extension
from codecs import open
from os import path
from distutils.core import setup


#### COMANDO PARA COMPILAR CYTHON
#### python setup.py build_ext --inplace


try:
	import numpy as np
except ImportError:
	exit("Por favor, primero instala una version superior a numpy 1.11.2 ¡Gracias!")


try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext

except ImportError:
    USAR_CYTHON = False
else:
    USAR_CYTHON = True


__version__ = '1.0.0'


aca = path.abspath(path.dirname(__file__))

with open(path.join(aca,'README.md'),encoding='utf-8') as a:
	descripcion = a.read()


# Dependencias
with open(path.join(aca,'requerimientos.txt'),encoding='utf-8') as a:
	requerimientos = a.read().split('\n')

instalar_requerimientos = [x.strip() for x in requerimientos if 'git+' not in x]
instalar_dependencias = [x.strip().replace('git+', '') for x in requerimientos if x.startswith('git+')]

cmdclass = {}

extension = '.pyx' if USAR_CYTHON else '.c'

extensiones = [

Extension('precisionpredictiva.algoritmos_predictivos.factorizacion_matricial',
	['precisionpredictiva/algoritmos_predictivos/factorizacion_matricial' + extension],
	include_dirs = [np.get_include()]),

Extension('precisionpredictiva.metricas_similitud',
	['precisionpredictiva/metricas_similitud' + extension],
	include_dirs = [np.get_include()]),

Extension('precisionpredictiva.algoritmos_predictivos.optimizador_sesgos',
	['precisionpredictiva/algoritmos_predictivos/optimizador_sesgos' + extension],
	include_dirs = [np.get_include()]),


]

if USAR_CYTHON:
	modulos_externos = cythonize(extensiones)
	cmdclass.update({'build_ext':build_ext})

else:
	modulos_externos = extensiones



setup(
	name='scikit-predictiveaccuracy',
	author='Marcos Dumón',
	author_email='mdumon11@gmail.com',
	description=('Predictive accuracy of recommendation system algorithms.'),
	version=__version__,
	license='GPLv3+',
	classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering',
       	'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
    ],
	packages=find_packages(exclude=['pruebas*']),
	include_package_data=True,
    ext_modules=modulos_externos,
    cmdclass=cmdclass,
    install_requires=instalar_requerimientos,
    dependency_links=instalar_dependencias

)


	

