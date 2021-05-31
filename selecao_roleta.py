import math
import random

from selecao import Selecao


class SelecaoRoleta(Selecao):
    __quantidade_cromossomos = 0.0


    def __valor_maximo(self):
        return (self.__quantidade_cromossomos + 1) * self.__quantidade_cromossomos / 2


    def __indice_por_valor(self, valor_sorteado):
        a = 1
        b = 1
        c = valor_sorteado * 2 * -1
        sol_1 = (-b - math.sqrt(b**2 - 4*a*c)) / (2 * a)
        sol_2 = (-b + math.sqrt(b**2 - 4*a*c)) / (2 * a)
        if not sol_1.is_integer():
            sol_1 = math.ceil(sol_1)
        if not sol_2.is_integer():
            sol_2 = math.ceil(sol_2)
        if sol_1 > 0:
            return int(self.__quantidade_cromossomos - sol_1)
        elif sol_2 > 0:
            return int(self.__quantidade_cromossomos - sol_2)
        else:
            return 0


    def __sorteia_indice(self):
        maior_valor_sorteio = self.__valor_maximo()
        valor_sorteado = random.randint(1, maior_valor_sorteio)
        indice_sorteado = self.__indice_por_valor(valor_sorteado) - 1
        return indice_sorteado


    def selecionar_cromossomo(self, populacao):
        self.__quantidade_cromossomos = len(populacao)
        indice_cromossomo = self.__sorteia_indice()
        return populacao[indice_cromossomo]