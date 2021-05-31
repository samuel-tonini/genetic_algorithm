import math
import random

from selecao import Selecao


class SelecaoTorneio(Selecao):
    def __init__(self, quantidade_participantes):
        self.__quantidade_participantes = quantidade_participantes


    def selecionar_cromossomo(self, populacao):
        quantidade_cromossomos = len(populacao)
        indices_participantes = [random.randint(1, quantidade_cromossomos) - 1 for _ in range(self.__quantidade_participantes)]
        indice_vendedor = min(indices_participantes)
        return populacao[indice_vendedor]