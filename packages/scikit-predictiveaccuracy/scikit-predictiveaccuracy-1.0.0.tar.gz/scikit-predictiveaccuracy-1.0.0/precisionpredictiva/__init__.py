from pkg_resources import get_distribution


from .algoritmos_predictivos import AlgoBase
from .algoritmos_predictivos import PredictorBase
from .algoritmos_predictivos import KNNPredictorBase
from .algoritmos_predictivos import SVD
from .algoritmos_predictivos import PrediccionImposible
from .algoritmos_predictivos import Prediccion
from .reader import Reader
from .datasets_incorporados import obtener_directorio_dataset
from .conjunto_entrenamiento import ConjuntoEntrenamiento
from . import iteradores
from . import dump
from .dataset import Dataset



__all__ = ['AlgoBase', 'PredictorBase', 'PrediccionImposible', 
			'Prediccion', 'Reader', 'ConjuntoEntrenamiento',
           'dump', 'obtener_directorio_dataset', 'iteradores','Dataset','KNNPredictorBase','SVD']


__version__ = get_distribution('scikit-predictiveaccuracy').version