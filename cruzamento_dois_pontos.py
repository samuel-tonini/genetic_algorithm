import random

from cruzamento import Cruzamento
import utilidades


class CruzamentoDoisPontos(Cruzamento):
    def __init__(self, quantidade_genes_por_cromossomo, cromossomo_utilidades):
        self.__quantidade_genes_por_cromossomo = quantidade_genes_por_cromossomo
        self.__cromossomo_utilidades = cromossomo_utilidades


    def realizar_cruzamento(self, cromossomo_pai, cromossomo_mae):
        resultado = []
        ponto_a = random.randint(1, self.__quantidade_genes_por_cromossomo)-1
        ponto_b = random.randint(1, self.__quantidade_genes_por_cromossomo)-1
        if ponto_a > ponto_b:
            ponto_a, ponto_b = ponto_b, ponto_a
        if utilidades.sorteio_premiado(50):
            resultado += cromossomo_pai[:ponto_a]
        else:
            resultado += cromossomo_mae[:ponto_a]
        if utilidades.sorteio_premiado(50):
            resultado += cromossomo_pai[ponto_a:ponto_b]
        else:
            resultado += cromossomo_mae[ponto_a:ponto_b]
        if utilidades.sorteio_premiado(50):
            resultado += cromossomo_pai[ponto_b:]
        else:
            resultado += cromossomo_mae[ponto_b:]
        resultado = self.__cromossomo_utilidades.ajustar_peso(resultado)
        return resultado