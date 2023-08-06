from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import namedtuple


class PrediccionImposible(Exception):
	pass


class Prediccion(namedtuple('Prediccion',['uid','iid','r_ui','r_hat','detalles'])):

    __slots__ = ()

    def __str__(self):
    	s = 'usuario: {uid:<10} '.format(uid=self.uid)
    	s += 'pelicula: {iid:<10} '.format(iid=self.iid)
    	if self.r_ui is not None:
    		s += 'r_ui = {r_ui:1.2f}  '.format(r_ui=self.r_ui)
    	else:
    		s += 'r_ui = None  '

    	s += 'r_hat = {r_hat:1.2f}  '.format(est=self.r_hat)
    	s += str(self.detalles)

    	return s