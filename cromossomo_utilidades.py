import math
import random

import utilidades


class CromossomoUtilidades:
    """Classe com métodos utilitários para a manipulação do cromossomo."""

    def __init__(self, itens_mochila, mochila_capacidade_maxima, percentual_maximo_mutacao, percentual_gene_mutar, quantidade_genes_por_cromossomo):
        """Parâmetros:

        itens_mochila = Dataframe com os itens da mochila;

        mochila_capacidade_maxima = Valor da capacidade máxima da mochila;

        percentual_maximo_mutacao = Percentual máximo de genes que poderam mutar no cromossomo;

        percentual_gene_mutar = Percentual que cada gene sorteado para mutação tem de realmente ser alterado;

        quantidade_genes_por_cromossomo = Quantidade de genes por cromossomo."""
        self.__itens_mochila = itens_mochila
        self.__mochila_capacidade_maxima = mochila_capacidade_maxima
        self.__percentual_maximo_mutacao = percentual_maximo_mutacao
        self.__percentual_gene_mutar = percentual_gene_mutar
        self.__quantidade_genes_por_cromossomo = quantidade_genes_por_cromossomo


    def indices_itens_carregados(self, cromossomo):
        """Retorna os indices dos genes que estão com valor 1 (um)."""
        resultado = []
        for i in range(len(cromossomo)):
            if cromossomo[i] == 1:
                resultado.append(i)
        return resultado


    def calcular_preco(self, cromossomo):
        """Calcula o preço do cromossomo."""
        indices_carregados = self.indices_itens_carregados(cromossomo)
        preco = 0.0
        for indice_carregado in indices_carregados:
            preco += self.__itens_mochila['preco'][indice_carregado]
        return preco


    def calcular_peso(self, cromossomo):
        """Calcula o peso do cromossomo."""
        indices_carregados = self.indices_itens_carregados(cromossomo)
        peso = 0.0
        for indice_carregado in indices_carregados:
            peso += self.__itens_mochila['peso'][indice_carregado]
        return peso


    def calcular_utilidade(self, cromossomo):
        """Calcula a utilidade do cromossomo."""
        indices_carregados = self.indices_itens_carregados(cromossomo)
        utilidade = 0.0
        for indice_carregado in indices_carregados:
            utilidade += self.__itens_mochila['utilidade'][indice_carregado]
        return utilidade


    def calcular_fitness(self, cromossomo):
        """Calcula o fitness do cromossomo."""
        indices_carregados = self.indices_itens_carregados(cromossomo)
        fitness = 0.0
        for indice_carregado in indices_carregados:
            fitness += self.__itens_mochila['utilidade'][indice_carregado] / self.__itens_mochila['preco'][indice_carregado]
        return fitness


    def ajustar_peso(self, cromossomo):
        """Ajusta o peso do cromossomo caso este esteja acima do peso máximo da mochila.
        Realiza este ajuste sorteando itens aleatoriamente para serem removidos da mochila."""
        resultado = cromossomo
        while self.calcular_peso(resultado) > self.__mochila_capacidade_maxima:
            indices_carregados = self.indices_itens_carregados(cromossomo)
            quantidade_itens_carregados = len(indices_carregados)
            indice_item_descarregar = random.randint(1, quantidade_itens_carregados) - 1
            resultado[indices_carregados[indice_item_descarregar]] = 0
        return resultado


    def mutar(self, cromossomo, indices_itens_tendenciosos):
        """Realiza a mutação em um cromossomo priorizando os genes tendenciosos (se houver).

        A quantidade de genes que serão sorteados respeita o parâmetro percentual_maximo_mutacao passado
        no construtor da classe e a probabilidade deste gene alterar é obtida pelo parâmetro percentual_gene_mutar,
        que também é informado no construtor."""
        resultado = cromossomo
        for _ in range(math.floor(self.__percentual_maximo_mutacao / 100 * self.__quantidade_genes_por_cromossomo)):
            if utilidades.sorteio_premiado(self.__percentual_gene_mutar):
                quantidade_itens_tendenciosos = len(indices_itens_tendenciosos)
                if quantidade_itens_tendenciosos > 0:
                    indice_gene_mutacao = random.randint(1, quantidade_itens_tendenciosos) - 1
                else:
                    indice_gene_mutacao = random.randint(1, self.__quantidade_genes_por_cromossomo) - 1
                if resultado[indice_gene_mutacao] == 1:
                    resultado[indice_gene_mutacao] = 0
                else:
                    resultado[indice_gene_mutacao] = 1
        resultado = self.ajustar_peso(resultado)
        return resultado