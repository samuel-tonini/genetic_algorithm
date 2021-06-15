import random

from populacao import Populacao


class PopulacaoAleatoria(Populacao):
    """Classe que implementa a geração de uma população totalmente aleatória."""

    def __init__(self, itens_mochila, mochila_capacidade_maxima, tamanho_populacao, quantidade_genes_por_cromossomo, cromossomo_utilidades):
        """Parâmetros:

        itens_mochila = Dataframe com os itens da mochila;

        mochila_capacidade_maxima = Valor da capacidade máxima da mochila;

        tamanho_populacao = Quantidade máxima de cromossomos na população;

        quantidade_genes_por_cromossomo = Quantidade de genes por cromossomo;

        cromossomo_utilidades = Instância da classe de utilidades para cromossomos."""
        self.__itens_mochila = itens_mochila
        self.__mochila_capacidade_maxima = mochila_capacidade_maxima
        self.__tamanho_populacao = tamanho_populacao
        self.__quantidade_genes_por_cromossomo = quantidade_genes_por_cromossomo
        self.__cromossomo_utilidades = cromossomo_utilidades


    def gerar_populacao(self, populacao_atual = [], percentual_mutacao = 0, contador_geracoes = 0):
        """Geração da população totalmente aleatória. O cromossomo é iniciado com todos os genes em zero,
        depois é sorteado aleatóriamente um item para adicionar ao cromossomo, quando o peso do item adicionado
        jutamente ao peso dos demais itens ultrapassa a capacidade máxima da mochila o item não é adicionado
        e o cromossomo é adicionado a população e inicia a geração de um novo cromossomo."""
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
