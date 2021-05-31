import math

import pandas as pd


class Tendencia:
    def __init__(self, percentual):
        self.__percentual_minimo = 100-percentual
        self.__percentual_maximo = percentual
    
    def calcular_indices_tendenciosos(self, populacao):
        tamanho_populacao = len(populacao)
        tendencia = pd.DataFrame(pd.DataFrame(populacao).mean(), columns=['media'])
        tendencia_valor_minimo = math.floor(self.__percentual_minimo / 100 * tamanho_populacao)
        tendencia_valor_maximo = math.floor(self.__percentual_maximo / 100 * tamanho_populacao)
        tendencia = tendencia[(tendencia['media'] < tendencia_valor_minimo) | (tendencia['media'] > tendencia_valor_maximo)]
        if tendencia.shape[0] == 0:
            tendencia_indices_tendenciosos = []
        else:
            tendencia_indices_tendenciosos = tendencia.index.tolist()
        return tendencia_indices_tendenciosos