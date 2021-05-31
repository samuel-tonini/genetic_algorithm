import math
import random

from populacao import Populacao


class PopulacaoMuLambda(Populacao):
    def __init__(self, tamanho_populacao, cruzamento, cromossomo_utilidades, selecao, tendencia):
        self.__tamanho_populacao = tamanho_populacao
        self.__cruzamento = cruzamento
        self.__cromossomo_utilidades = cromossomo_utilidades
        self.__selecao = selecao
        self.__tendencia = tendencia


    def gerar_populacao(self, populacao_atual, percentual_mutacao):
        quantidade_mutacoes = math.floor(percentual_mutacao / self.__tamanho_populacao * 100)
        filhos = []
        for _ in range(self.__tamanho_populacao):
            cromossomo_pai = self.__selecao.selecionar_cromossomo(populacao_atual)
            cromossomo_mae = self.__selecao.selecionar_cromossomo(populacao_atual)
            filho_cruzamento_atual = self.__cruzamento.realizar_cruzamento(cromossomo_pai, cromossomo_mae)
            filhos.append(filho_cruzamento_atual)
        if quantidade_mutacoes > 0:
            indices_itens_tendenciosos = self.__tendencia.calcular_indices_tendenciosos(populacao_atual + filhos)
        for i in range(quantidade_mutacoes):
            indice_para_mutacao = random.randint(1, self.__tamanho_populacao) - 1
            cromossomo_para_mutacao = filhos[indice_para_mutacao]
            filhos[indice_para_mutacao] = self.__cromossomo_utilidades.mutar(cromossomo_para_mutacao, indices_itens_tendenciosos)
        return populacao_atual + filhos
