from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numbers
import numpy as np


def generador_aleatorio(random_state):

    if random_state is None:
        return np.random.mtrand._rand
    
    elif isinstance(random_state, (numbers.Integral, np.integer)):
        return np.random.RandomState(random_state)
    
    if isinstance(random_state, np.random.RandomState):
        return random_state
    
    raise ValueError('Estado aleatorio incorrecto. Se esperaba None, int o numpy '
                     'Instancia RandomState, obtuvo un '
                     '{}'.format(type(random_state)))