
from __future__ import (absolute_import, division, print_function,unicode_literals)
import numpy as np
from six.moves import range
cimport numpy as np 


from .algo_base import AlgoBase
from .predicciones import PrediccionImposible
from .. utilidades import generador_aleatorio



class SVD(AlgoBase):

    def __init__(self, 
                    n_factores=100, 
                    n_epocas=20,
                    sesgado=False,
                    promedio_inicial=0,
                    desv_stand_inicial=0.1, 
                    tasas_aprend=0.005,
                    tasas_reg=0.02, 
                    t_aprend_bu=None,t_aprend_bi=None, 
                    t_aprend_pu=None, t_aprend_qi=None,
                    t_reg_bu=None,
                    t_reg_bi=None, 
                    t_reg_pu=None, 
                    t_reg_qi=None,random_state=None,verbose=True):

        self.n_factores = n_factores
        self.n_epocas = n_epocas
        self.sesgado = sesgado
        self.promedio_inicial = promedio_inicial
        self.desv_stand_inicial = desv_stand_inicial
        self.t_aprend_bu = t_aprend_bu if t_aprend_bu is not None else tasas_aprend
        self.t_aprend_bi = t_aprend_bi if t_aprend_bi is not None else tasas_aprend
        self.t_aprend_pu = t_aprend_pu if t_aprend_pu is not None else tasas_aprend
        self.t_aprend_qi = t_aprend_qi if t_aprend_qi is not None else tasas_aprend
        self.t_reg_bu = t_reg_bu if t_reg_bu is not None else tasas_reg
        self.t_reg_bi = t_reg_bi if t_reg_bi is not None else tasas_reg
        self.t_reg_pu = t_reg_pu if t_reg_pu is not None else tasas_reg
        self.t_reg_qi = t_reg_qi if t_reg_qi is not None else tasas_reg
        self.random_state = random_state
        self.verbose = verbose



        AlgoBase.__init__(self)



    def ajustar_modelo(self, entradas_entrenamiento):
        AlgoBase.ajustar_modelo(self,entradas_entrenamiento)
        self.sgd(entradas_entrenamiento)
        
        return self



    def sgd(self,entradas_entrenamiento):
        
        cdef np.ndarray[np.double_t] b_u
        cdef np.ndarray[np.double_t] b_i
        cdef np.ndarray[np.double_t,ndim=2] p_u
        cdef np.ndarray[np.double_t,ndim=2] q_i

        cdef int usuario, pelicula, f
        cdef double califiacion, error, prod_escalar, pu_act, qi_act
        cdef double promedio_global = self.conjunto_entrenamiento.promedio_global

        cdef double  ta_bu = self.t_aprend_bu
        cdef double  ta_bi = self.t_aprend_bi
        cdef double  ta_pu = self.t_aprend_pu
        cdef double  ta_qi = self.t_aprend_qi

        cdef double tr_bu = self.t_reg_bu
        cdef double tr_bi = self.t_reg_bi
        cdef double tr_pu = self.t_reg_pu
        cdef double tr_qi = self.t_reg_qi

        ga = generador_aleatorio(self.random_state)
        
        b_u = np.zeros(entradas_entrenamiento.n_usuarios, np.double)
        
        b_i = np.zeros(entradas_entrenamiento.n_peliculas, np.double)
        
        p_u = ga.uniform(self.promedio_inicial, 
            self.desv_stand_inicial,
            (entradas_entrenamiento.n_usuarios, self.n_factores))
        
        q_i = ga.uniform(self.promedio_inicial, 
            self.desv_stand_inicial,
            (entradas_entrenamiento.n_peliculas, self.n_factores))

        if not self.sesgado:
            promedio_global = 0
        
        for epoca_actual in range(self.n_epocas):
            if self.verbose:
                print("Procesando época {}".format(epoca_actual))
            
            for usuario, pelicula, calificacion in entradas_entrenamiento.todas_calificaciones():
                
                prod_escalar = 0 
                
                for f in range(self.n_factores):
                    prod_escalar += q_i[pelicula,f] * p_u[usuario,f] 
                error = calificacion - (promedio_global + b_u[usuario] + b_i[pelicula] + prod_escalar)

                if self.sesgado:
                    b_u[usuario] += ta_bu * (error - tr_bu * b_u[usuario])
                    b_i[pelicula] += ta_bi * (error - tr_bi * b_i[pelicula]) 
                
                for f in range(self.n_factores):
                    pu_act = p_u[usuario,f]
                    qi_act = q_i[pelicula,f]
                    p_u[usuario,f]  += ta_pu * (error * qi_act - tr_pu * pu_act)
                    q_i[pelicula,f] += ta_qi * (error * pu_act - tr_qi * qi_act)
        
        self.b_u = b_u
        self.b_i = b_i
        self.p_u = p_u
        self.q_i = q_i
    
    

    def estimar(self, usuario, pelicula):
        
        existe_usuario = self.conjunto_entrenamiento.existe_usuario(usuario)
        existe_pelicula = self.conjunto_entrenamiento.existe_pelicula(pelicula)

        if self.sesgado:
            r_hat = self.conjunto_entrenamiento.promedio_global

            
            if existe_usuario:
                r_hat += self.b_u[usuario]
            
            
            if existe_pelicula:
                r_hat += self.b_i[pelicula]
            
            
            if existe_usuario and existe_pelicula:
                r_hat += np.dot(self.q_i[pelicula], self.p_u[usuario])
        

        else:
            if existe_usuario and existe_pelicula:
                r_hat = np.dot(self.q_i[pelicula], self.p_u[usuario])
            else:
                raise PrediccionImposible("El usuario y la película son desconcidos")
        
        return r_hat 











































































































