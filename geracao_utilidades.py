import os

import pandas as pd


class GeracaoUtilidades:
    """Classe com métodos utilitários para a manipulação das gerações."""

    def __init__(self, separador_dados, prefixo_melhores, prefixo_geracao, cromossomo_utilidades, mochila_capacidade_maxima, populacao_quantidade_cromossomos):
        """Parâmetros:

        separador_dados = Caracter para separação de dados ao salvar o arquivo;

        prefixo_melhores = Prefixo para o nome do arquivo com os melhores resulados;

        prefixo_geracao = Prefixo para o nome do arquivo com os dados da geração completa;

        cromossomo_utilidades = Instância da classe de utilidades para cromossomos;

        mochila_capacidade_maxima = Valor da capacidade máxima da mochila;

        populacao_quantidade_cromossomos = Quantidade máxima de cromossomos na população."""
        self.__separador_dados = separador_dados
        self.__prefixo_melhores = prefixo_melhores
        self.__prefixo_geracao = prefixo_geracao
        self.__cromossomo_utilidades = cromossomo_utilidades
        self.__mochila_capacidade_maxima = mochila_capacidade_maxima
        self.__populacao_quantidade_cromossomos = populacao_quantidade_cromossomos


    def salvar_melhor(self, dados_geracao, contador_execucoes):
        """Método para salvar o melhor resultado da geração."""
        caminho_arquivo = '{}_{}.csv'.format(self.__prefixo_melhores, contador_execucoes)
        if os.path.exists(caminho_arquivo):
            melhores = pd.read_csv(caminho_arquivo, sep=self.__separador_dados)
        else:
            melhores = pd.DataFrame(columns=['solucao', 'peso', 'utilidade', 'preco', 'fitness'])
        melhores.loc[melhores.shape[0]] = dados_geracao.loc[0]
        melhores.to_csv(caminho_arquivo, sep=self.__separador_dados, index=False)


    def salvar_geracao(self, dados_geracao, contador_execucoes, contador_geracoes):
        """Método para salvar toda geração."""
        caminho_arquivo = '{}_{}_{}.csv'.format(self.__prefixo_geracao, contador_execucoes, contador_geracoes)
        dados_geracao.to_csv(caminho_arquivo, sep=self.__separador_dados, index=False)


    def apurar_geracao(self, populacao):
        """Método apurar o fitness da geração e retorna os valores ordenados de maneira
        decrescente e caso a população esteja maior que o tamanho máximo apenas os valores
        até o tamanho máximo da população será retornado."""
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


    def remover_duplicados(self, geracao):
        geracao_sem_duplicados = geracao.drop_duplicates(subset=['peso', 'utilidade', 'preco', 'fitness'], keep='first')
        return geracao_sem_duplicados