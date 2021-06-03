import math
import random

from selecao import Selecao


class SelecaoTorneio(Selecao):
    """Classe que implementa seleção dos genes por torneio."""

    def __init__(self, quantidade_participantes):
        """Parâmetros:

        quantidade_participantes = Quantidade de participantes do torneio."""
        self.__quantidade_participantes = quantidade_participantes


    def selecionar_cromossomo(self, populacao):
        """Escolhe aleatoriamente os participantes do torneio e define o campeão pelo menor
        índice, uma vez que os melhores da população são os primeiros itens."""
        quantidade_cromossomos = len(populacao)
        indices_participantes = [random.randint(1, quantidade_cromossomos) - 1 for _ in range(self.__quantidade_participantes)]
        indice_vendedor = min(indices_participantes)
        return populacao[indice_vendedor]