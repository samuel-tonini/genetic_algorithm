import math
import random

from populacao import Populacao


class PopulacaoPreencher(Populacao):
    """Classe que implementa a geração apenas técnica de cruzamento e seleção,
    apenas para preenchimento da população."""

    def __init__(self, tamanho_populacao, cruzamento, cromossomo_utilidades, selecao):
        """Parâmetros:

        tamanho_populacao = Quantidade máxima de cromossomos na população;

        cruzamento = Instância da classe que implementa a técnica de cruzamento utilizada e 
        herda da classe base Cruzamento;

        cromossomo_utilidades = Instância da classe de utilidades para cromossomos

        selecao = Instância da classe que implementa a técnica de seleção utilizada e 
        herda da classe base Seleção."""
        self.__tamanho_populacao = tamanho_populacao
        self.__cruzamento = cruzamento
        self.__cromossomo_utilidades = cromossomo_utilidades
        self.__selecao = selecao


    def gerar_populacao(self, populacao_atual, percentual_mutacao = 0.0, contador_geracoes = 0):
        """Preenchimento de uma população que estaja abaixo da quantidade de indivíduos defina para
        execução, utilizando apenas as técnicas de cruzamento e seleção."""
        tamanho_populacao_atual = len(populacao_atual)
        quantidade_novos_individuos = self.__tamanho_populacao - tamanho_populacao_atual
        filhos = []
        for _ in range(quantidade_novos_individuos):
            cromossomo_pai = self.__selecao.selecionar_cromossomo(populacao_atual)
            cromossomo_mae = self.__selecao.selecionar_cromossomo(populacao_atual)
            filho_cruzamento_atual = self.__cruzamento.realizar_cruzamento(cromossomo_pai, cromossomo_mae)
            filhos.append(filho_cruzamento_atual)
        return populacao_atual + filhos
