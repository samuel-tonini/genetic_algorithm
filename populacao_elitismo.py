import math
import random

from populacao import Populacao


class PopulacaoElitismo(Populacao):
    """Classe que implementa a geração de uma população utilizando a técnica de Elitismo."""

    def __init__(self, tamanho_populacao, percentual_sobreviventes, cruzamento, cromossomo_utilidades, selecao, tendencia):
        """Parâmetros:

        tamanho_populacao = Quantidade máxima de cromossomos na população;

        percentual_sobreviventes = Percentual dos genes que irão sobreviver para a próxima geração;

        cruzamento = Instância da classe que implementa a técnica de cruzamento utilizada e 
        herda da classe base Cruzamento;

        cromossomo_utilidades = Instância da classe de utilidades para cromossomos

        selecao = Instância da classe que implementa a técnica de seleção utilizada e 
        herda da classe base Seleção;

        tendencia = Instância da classe que implementa a técnica que calcula os genes tedenciosos."""
        self.__tamanho_populacao = tamanho_populacao
        self.__percentual_sobreviventes = percentual_sobreviventes
        self.__cruzamento = cruzamento
        self.__cromossomo_utilidades = cromossomo_utilidades
        self.__selecao = selecao
        self.__tendencia = tendencia
        self.__indices_itens_tendenciosos = []


    def gerar_populacao(self, populacao_atual, percentual_mutacao, contador_geracoes):
        """Geração da população por Elitismo onde o percentual de sobreviventes é definido pelo parâmetro percentual_sobreviventes
        os demais indivíduos serão gerados utilizando as técnicas de seleção e cruzamento repassadas no construtor.
        Caso haja uma taxa de mutação a mesma realiza sorteio apenas nos filhos gerados.
        Por fim retorna os sobreviventes e os filhos gerados."""
        quantidade_sobreviventes = math.floor(self.__tamanho_populacao * self.__percentual_sobreviventes / 100)
        quantidade_novos_individuos = self.__tamanho_populacao - quantidade_sobreviventes
        quantidade_mutacoes = math.floor(percentual_mutacao / quantidade_novos_individuos * 100)
        melhores_populacao_atual = populacao_atual[:quantidade_sobreviventes]
        filhos = []
        for _ in range(quantidade_novos_individuos):
            cromossomo_pai = self.__selecao.selecionar_cromossomo(populacao_atual)
            cromossomo_mae = self.__selecao.selecionar_cromossomo(populacao_atual)
            filho_cruzamento_atual = self.__cruzamento.realizar_cruzamento(cromossomo_pai, cromossomo_mae)
            filhos.append(filho_cruzamento_atual)
        if contador_geracoes % self.__tendencia.frequencia_execucao == 0:
            self.__indices_itens_tendenciosos = self.__tendencia.calcular_indices_tendenciosos(melhores_populacao_atual + filhos)
        for i in range(quantidade_mutacoes):
            indice_para_mutacao = random.randint(1, quantidade_novos_individuos) - 1
            cromossomo_para_mutacao = filhos[indice_para_mutacao]
            filhos[indice_para_mutacao] = self.__cromossomo_utilidades.mutar(cromossomo_para_mutacao, self.__indices_itens_tendenciosos)
        return melhores_populacao_atual + filhos
