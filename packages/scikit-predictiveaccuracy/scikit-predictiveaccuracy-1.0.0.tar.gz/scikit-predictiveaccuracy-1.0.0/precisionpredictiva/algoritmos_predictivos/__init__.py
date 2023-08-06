
from .algo_base import AlgoBase
from .predictor_base import PredictorBase
from .factorizacion_matricial import SVD
from .knn import KNNPredictorBase
from .predicciones import PrediccionImposible
from .predicciones import Prediccion





__all__ = ['AlgoBase', 
			'PredictorBase', 
			'PrediccionImposible', 
			'Prediccion',
			'KNNPredictorBase','SVD']