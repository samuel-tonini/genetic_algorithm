import math

from cruzamento import Cruzamento
import utilidades


class CruzamentoUniforme(Cruzamento):
    """Classe que implementa a técnica de cruzamento uniforme."""

    def __init__(self, quantidade_genes_por_cromossomo, quantidade_genes_por_grupo, cromossomo_utilidades):
        """Parâmetros:

        quantidade_genes_por_cromossomo = Quantidade de genes por cromossomo;

        quantidade_genes_por_grupo = Quantidade de genes que serão levados em cada sorteio;

        cromossomo_utilidades = Instância da classe de utilidades para cromossomos."""
        self.__quantidade_genes_por_cromossomo = quantidade_genes_por_cromossomo
        self.__quantidade_genes_por_grupo = quantidade_genes_por_grupo
        self.__cromossomo_utilidades = cromossomo_utilidades


    def __genes_do_grupo(self, cromossomo, grupo):
        """Retorna os genes pelo grupo seguinto a quantidade de genes defino no parâmetro 
        quantidade_genes_por_grupo informado no construtor."""
        resultado = []
        for i in range(self.__quantidade_genes_por_grupo):
            resultado.append(cromossomo[grupo * self.__quantidade_genes_por_grupo + i])
        return resultado


    def realizar_cruzamento(self, cromossomo_pai, cromossomo_mae):
        """Cruza dois cromossomos utilizando o cruzamento uniforme.

        Divide a quantidade de genes do cromossomo pela quantidade de genes de cada grupo
        e depois sorteia qual será a origem de cada grupo do pai ou da mãe com a mesma probabilidade.
        No final é feito um ajuste no peso do cromossomo para que o mesmo seja válido perante a
        restrição de peso máximo da mochila."""
        resultado = []
        for i in range(math.floor(self.__quantidade_genes_por_cromossomo/self.__quantidade_genes_por_grupo)):
            genes_a = self.__genes_do_grupo(cromossomo_pai, i)
            genes_b = self.__genes_do_grupo(cromossomo_mae, i)
            if utilidades.sorteio_premiado(50):
                resultado += genes_a
            else:
                resultado += genes_b
        quantidade_genes_faltando = self.__quantidade_genes_por_cromossomo - len(resultado)
        if quantidade_genes_faltando != 0:
            if utilidades.sorteio_premiado(50):
                resultado += cromossomo_pai[-quantidade_genes_faltando:]
            else:
                resultado += cromossomo_mae[-quantidade_genes_faltando:]
        resultado = self.__cromossomo_utilidades.ajustar_peso(resultado)
        return resultado
