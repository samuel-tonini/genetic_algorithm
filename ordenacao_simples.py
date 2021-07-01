import pandas as pd

from ordenacao import Ordenacao


class OrdenacaoSimples(Ordenacao):
    """Classe base para implementação das técnicas de ordenação com único objetivo da população."""

    def __init__(self, cromossomo_utilidades, mochila_capacidade_maxima, populacao_quantidade_cromossomos):
        """Parâmetros:

        cromossomo_utilidades = Instância da classe de utilidades para cromossomos;

        mochila_capacidade_maxima = Valor da capacidade máxima da mochila;

        populacao_quantidade_cromossomos = Quantidade máxima de cromossomos na população."""
        self.__cromossomo_utilidades = cromossomo_utilidades
        self.__mochila_capacidade_maxima = mochila_capacidade_maxima
        self.__populacao_quantidade_cromossomos = populacao_quantidade_cromossomos

    def ordenar_populacao(self, populacao):
        """Inicio da ordenação multiobjetivo calcula as frentes."""
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