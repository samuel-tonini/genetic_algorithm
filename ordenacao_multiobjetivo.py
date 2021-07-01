import pandas as pd

from ordenacao import Ordenacao


class OrdenacaoMultiobjetivo(Ordenacao):
    """Classe base para implementação das técnicas de ordenação multiobjetivo da população."""

    def __init__(self, cromossomo_utilidades, mochila_capacidade_maxima, populacao_quantidade_cromossomos):
        """Parâmetros:

        mochila_capacidade_maxima = Valor da capacidade máxima da mochila;

        cromossomo_utilidades = Instância da classe de utilidades para cromossomos;

        populacao_quantidade_cromossomos = Quantidade máxima de cromossomos na população."""
        self.__mochila_capacidade_maxima = mochila_capacidade_maxima
        self.__cromossomo_utilidades = cromossomo_utilidades
        self.__populacao_quantidade_cromossomos = populacao_quantidade_cromossomos

    def ordenar_populacao(self, populacao):
        """Inicio da ordenação multiobjetivo calcula as frentes."""
        resultado = pd.DataFrame(columns=['solucao', 'peso', 'utilidade', 'preco', 'fitness', 'metodo'])

        for i in range(len(populacao)):
            cromossomo = populacao[i]
            cromossomo_peso = round(self.__cromossomo_utilidades.calcular_peso(cromossomo), 2)
            cromossomo_preco = round(self.__cromossomo_utilidades.calcular_preco(cromossomo), 2)
            cromossomo_utilidade = round(self.__cromossomo_utilidades.calcular_utilidade(cromossomo), 2)
            resultado.loc[i] = [cromossomo, cromossomo_peso, cromossomo_utilidade, cromossomo_preco, 0, 0.00]

        lista_utilidades = sorted(resultado['utilidade'].unique(), reverse=True)
        lista_pesos = sorted(resultado['peso'].unique())
        lista_precos = sorted(resultado['preco'].unique())

        intervalo_utilidade = max(lista_utilidades) - min(lista_utilidades)
        intervalo_peso = max(lista_pesos) - min(lista_pesos)
        intervalo_preco = max(lista_precos) - min(lista_precos)

        for i in range(len(resultado)):
            qualidade = 0
            peso_atual = resultado.loc[i]['peso']
            preco_atual = resultado.loc[i]['preco']
            utilidade_atual = resultado.loc[i]['utilidade']

            melhores = resultado[(resultado['peso'] <= peso_atual) & (resultado['preco'] <= preco_atual) & (resultado['utilidade'] >= utilidade_atual)]
            melhores = melhores[(melhores['peso'] < peso_atual) | (melhores['preco'] < preco_atual) | (melhores['utilidade'] > utilidade_atual)]

            resultado.iloc[i, resultado.columns.get_loc('fitness')] = melhores.shape[0]

            if utilidade_atual == min(lista_utilidades):
                distancia_utilidade = lista_utilidades[1] - lista_utilidades[0] / intervalo_utilidade
            elif utilidade_atual == max(lista_utilidades):
                distancia_utilidade = lista_utilidades[-1] - lista_utilidades[-2] / intervalo_utilidade
            else:
                indice_utilidade = lista_utilidades.index(utilidade_atual)
                distancia_utilidade = lista_utilidades[indice_utilidade-1] - lista_utilidades[indice_utilidade+1] / intervalo_utilidade

            if peso_atual == min(lista_pesos):
                distancia_peso = lista_pesos[1] - lista_pesos[0] / intervalo_peso
            elif peso_atual == max(lista_pesos):
                distancia_peso = lista_pesos[-2] - lista_pesos[-1] / intervalo_peso
            else:
                indice_peso = lista_pesos.index(peso_atual)
                distancia_peso = lista_pesos[indice_peso+1] - lista_pesos[indice_peso-1] / intervalo_peso

            if preco_atual == min(lista_precos):
                distancia_preco = lista_precos[1] - lista_precos[0] / intervalo_preco
            elif preco_atual == max(lista_precos):
                distancia_preco = lista_precos[-2] - lista_precos[-1] / intervalo_preco
            else:
                indice_preco = lista_precos.index(preco_atual)
                distancia_preco = lista_precos[indice_preco+1] - lista_precos[indice_preco-1] / intervalo_preco

            resultado.iloc[i, resultado.columns.get_loc('metodo')] = distancia_utilidade + distancia_peso + distancia_preco

        resultado = resultado[(resultado['peso'] <= self.__mochila_capacidade_maxima) & (resultado['peso'] > 0.0)].sort_values(by=['fitness', 'metodo'], ascending=[True, False]).reset_index(drop=True)
        if resultado.shape[0] > self.__populacao_quantidade_cromossomos:
            resultado = resultado[:self.__populacao_quantidade_cromossomos]

        return resultado
