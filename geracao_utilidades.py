import os

import pandas as pd


class GeracaoUtilidades:
    def __init__(self, separador_dados, prefixo_melhores, prefixo_geracao, cromossomo_utilidades, mochila_capacidade_maxima, populacao_quantidade_cromossomos):
        self.__separador_dados = separador_dados
        self.__prefixo_melhores = prefixo_melhores
        self.__prefixo_geracao = prefixo_geracao
        self.__cromossomo_utilidades = cromossomo_utilidades
        self.__mochila_capacidade_maxima = mochila_capacidade_maxima
        self.__populacao_quantidade_cromossomos = populacao_quantidade_cromossomos


    def salvar_melhor(self, dados_geracao, contador_execucoes):
        caminho_arquivo = '{}_{}.csv'.format(self.__prefixo_melhores, contador_execucoes)
        if os.path.exists(caminho_arquivo):
            melhores = pd.read_csv(caminho_arquivo, sep=self.__separador_dados)
        else:
            melhores = pd.DataFrame(columns=['solucao', 'peso', 'utilidade', 'preco', 'fitness'])
        melhores.loc[melhores.shape[0]] = dados_geracao.loc[0]
        melhores.to_csv(caminho_arquivo, sep=self.__separador_dados, index=False)


    def salvar_geracao(self, dados_geracao, contador_execucoes, contador_geracoes):
        caminho_arquivo = '{}_{}_{}.csv'.format(self.__prefixo_geracao, contador_execucoes, contador_geracoes)
        dados_geracao.to_csv(caminho_arquivo, sep=self.__separador_dados, index=False)


    def apurar_geracao(self, populacao):
        resultado = pd.DataFrame(columns=['solucao', 'peso', 'utilidade', 'preco', 'fitness'])
        for i in range(len(populacao)):
            cromossomo = populacao[i]
            cromossomo_peso = self.__cromossomo_utilidades.calcular_peso(cromossomo)
            cromossomo_preco = self.__cromossomo_utilidades.calcular_preco(cromossomo)
            cromossomo_utilidade = self.__cromossomo_utilidades.calcular_utilidade(cromossomo)
            cromossomo_fitness = self.__cromossomo_utilidades.calcular_fitness(cromossomo)
            resultado.loc[i] = [cromossomo, cromossomo_peso, cromossomo_utilidade, cromossomo_preco, cromossomo_fitness]
        resultado = resultado[resultado['peso'] <= self.__mochila_capacidade_maxima].sort_values('fitness', ascending=False).reset_index(drop=True)
        if resultado.shape[0] > self.__populacao_quantidade_cromossomos:
            resultado = resultado[:self.__populacao_quantidade_cromossomos]
        return resultado