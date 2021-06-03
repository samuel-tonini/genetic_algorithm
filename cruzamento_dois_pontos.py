import random

from cruzamento import Cruzamento
import utilidades


class CruzamentoDoisPontos(Cruzamento):
    """Classe que implementa a técnica de cruzamento de dois pontos."""

    def __init__(self, quantidade_genes_por_cromossomo, cromossomo_utilidades):
        """Parâmetros:

        quantidade_genes_por_cromossomo = Quantidade de genes por cromossomo;

        cromossomo_utilidades = Instância da classe de utilidades para cromossomos."""
        self.__quantidade_genes_por_cromossomo = quantidade_genes_por_cromossomo
        self.__cromossomo_utilidades = cromossomo_utilidades


    def realizar_cruzamento(self, cromossomo_pai, cromossomo_mae):
        """Cruza dois cromossomos utilizando a técnica de dois pontos.

        Seleciona dois pontos aleatoriamente para serem os pontos de corte dos cromossomos, após isso
        sorteia com a mesma probabilidade se qual será a origem de cada seção do pai ou da mãe.
        No final é feito um ajuste no peso do cromossomo para que o mesmo seja válido perante a
        restrição de peso máximo da mochila."""
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