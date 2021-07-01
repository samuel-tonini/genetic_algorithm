import os

import pandas as pd


class GeracaoUtilidades:
    """Classe com métodos utilitários para a manipulação das gerações."""

    def __init__(self, separador_dados, prefixo_melhores, prefixo_geracao, cromossomo_utilidades, mochila_capacidade_maxima, populacao_quantidade_cromossomos, multiobjetivo, prefixo_melhores_multiobjetivo):
        """Parâmetros:

        separador_dados = Caracter para separação de dados ao salvar o arquivo;

        prefixo_melhores = Prefixo para o nome do arquivo com os melhores resulados;

        prefixo_geracao = Prefixo para o nome do arquivo com os dados da geração completa;

        cromossomo_utilidades = Instância da classe de utilidades para cromossomos;

        mochila_capacidade_maxima = Valor da capacidade máxima da mochila;

        populacao_quantidade_cromossomos = Quantidade máxima de cromossomos na população;

        multiobjetivo = Se a execução será feita usando um cretério multiobjetivo;

        prefixo_melhores_multiobjetivo = Prefixo para o nome do arquivo com os melhores resulados multiobjetivo."""
        self.__separador_dados = separador_dados
        self.__prefixo_melhores = prefixo_melhores
        self.__prefixo_geracao = prefixo_geracao
        self.__cromossomo_utilidades = cromossomo_utilidades
        self.__mochila_capacidade_maxima = mochila_capacidade_maxima
        self.__populacao_quantidade_cromossomos = populacao_quantidade_cromossomos
        self.__multiobjetivo = multiobjetivo
        self.__prefixo_melhores_multiobjetivo = prefixo_melhores_multiobjetivo


    def salvar_melhor(self, dados_geracao, contador_execucoes):
        """Método para salvar o melhor resultado da geração."""
        caminho_arquivo = '{}_{}.csv'.format(self.__prefixo_melhores, contador_execucoes)
        if os.path.exists(caminho_arquivo):
            melhores = pd.read_csv(caminho_arquivo, sep=self.__separador_dados)
        elif self.__multiobjetivo:
            melhores = pd.DataFrame(columns=['solucao', 'peso', 'utilidade', 'preco', 'fitness', 'metodo'])
        else:
            melhores = pd.DataFrame(columns=['solucao', 'peso', 'utilidade', 'preco', 'fitness'])
        melhores.loc[melhores.shape[0]] = dados_geracao.loc[0]
        melhores.to_csv(caminho_arquivo, sep=self.__separador_dados, index=False)


    def salvar_geracao(self, dados_geracao, contador_execucoes, contador_geracoes):
        """Método para salvar toda geração."""
        caminho_arquivo = '{}_{}_{}.csv'.format(self.__prefixo_geracao, contador_execucoes, contador_geracoes)
        dados_geracao.to_csv(caminho_arquivo, sep=self.__separador_dados, index=False)


    def remover_duplicados(self, geracao):
        if self.__multiobjetivo:
            geracao_sem_duplicados = geracao.drop_duplicates(subset=['peso', 'utilidade', 'preco', 'fitness', 'metodo'], keep='first')
        else:
            geracao_sem_duplicados = geracao.drop_duplicates(subset=['peso', 'utilidade', 'preco', 'fitness'], keep='first')
        return geracao_sem_duplicados


    def salvar_melhores_multiobjetivo(self, dados_geracao, contador_execucoes):
        """Método para salvar o melhor resultado da geração."""
        caminho_arquivo = '{}_{}.csv'.format(self.__prefixo_melhores_multiobjetivo, contador_execucoes)
        dados_geracao[dados_geracao['fitness'] == 0].to_csv(caminho_arquivo, sep=self.__separador_dados, index=False)


    def calcular_ahp(self, dados_geracao, matriz_julgamento_ahp):
        total_criterio_utilidade = 1 + matriz_julgamento_ahp['utilidade']['preco'] + matriz_julgamento_ahp['utilidade']['peso']
        total_criterio_preco = (1 / matriz_julgamento_ahp['utilidade']['preco']) + 1 + (1 / matriz_julgamento_ahp['peso']['preco'])
        total_criterio_peso = (1 / matriz_julgamento_ahp['utilidade']['peso']) + matriz_julgamento_ahp['peso']['preco'] + 1
        peso_criterio_utilidade = ((1 / total_criterio_utilidade) + ((1 / matriz_julgamento_ahp['utilidade']['preco']) / total_criterio_utilidade) + ((1 / matriz_julgamento_ahp['utilidade']['peso']) / total_criterio_utilidade)) / 3
        peso_criterio_preco = ((1 / total_criterio_preco) + (matriz_julgamento_ahp['utilidade']['preco'] / total_criterio_preco) + ((1 / matriz_julgamento_ahp['peso']['preco']) / total_criterio_preco)) / 3
        peso_criterio_peso = ((1 / total_criterio_peso) + (matriz_julgamento_ahp['utilidade']['peso'] / total_criterio_peso) + (matriz_julgamento_ahp['peso']['preco'] / total_criterio_peso)) / 3

        dados_geracao['ahp'] = 0.0

        for i in range(len(dados_geracao)):
            peso_atual = round(dados_geracao.loc[i]['peso'], 2)
            preco_atual = round(dados_geracao.loc[i]['preco'], 2)
            utilidade_atual = round(dados_geracao.loc[i]['utilidade'], 2)
            dados_geracao.iloc[i, dados_geracao.columns.get_loc('ahp')] = (utilidade_atual * peso_criterio_utilidade)  + (preco_atual * peso_criterio_preco) + (peso_atual * peso_criterio_peso)

        return dados_geracao


    def calcular_borda(self, dados_geracao):
        lista_utilidades =  sorted(dados_geracao['utilidade'].unique(), reverse=True)
        lista_pesos = sorted(dados_geracao['peso'].unique())
        lista_precos = sorted(dados_geracao['preco'].unique())

        dados_geracao['borda'] = 0.0

        for i in range(len(dados_geracao)):
            peso_atual = round(dados_geracao.loc[i]['peso'], 2)
            preco_atual = round(dados_geracao.loc[i]['preco'], 2)
            utilidade_atual = round(dados_geracao.loc[i]['utilidade'], 2)
            dados_geracao.iloc[i, dados_geracao.columns.get_loc('borda')] = (lista_utilidades.index(utilidade_atual) + 1)  + (lista_utilidades.index(utilidade_atual) * preco_atual) + (lista_utilidades.index(utilidade_atual) * peso_atual)

        return dados_geracao
