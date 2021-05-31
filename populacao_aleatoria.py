import random

from populacao import Populacao


class PopulacaoAleatoria(Populacao):
    def __init__(self, itens_mochila, mochila_capacidade_maxima, tamanho_populacao, quantidade_genes_por_cromossomo, cromossomo_utilidades):
        self.__itens_mochila = itens_mochila
        self.__mochila_capacidade_maxima = mochila_capacidade_maxima
        self.__tamanho_populacao = tamanho_populacao
        self.__quantidade_genes_por_cromossomo = quantidade_genes_por_cromossomo
        self.__cromossomo_utilidades = cromossomo_utilidades


    def gerar_populacao(self, populacao_atual = [], percentual_mutacao = 0):
        resultado = []
        for i in range(self.__tamanho_populacao):
            cromossomo = [0 for _ in range(self.__quantidade_genes_por_cromossomo)]
            while True:
                indice_item_carregar = random.randint(1, self.__quantidade_genes_por_cromossomo)-1
                peso_item_carregar = self.__itens_mochila['peso'][indice_item_carregar]
                peso_atual_cromossomo = self.__cromossomo_utilidades.calcular_peso(cromossomo)
                if (peso_atual_cromossomo+peso_item_carregar) < self.__mochila_capacidade_maxima:
                    cromossomo[indice_item_carregar] = 1
                else:
                    break
            resultado.append(cromossomo)
        return resultado
