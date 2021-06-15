from abc import ABCMeta, abstractmethod

class Populacao(metaclass=ABCMeta):
    """Classe base para implementação das técnicas de geração de população."""

    @abstractmethod
    def gerar_populacao(self, populacao_atual, percentual_mutacao, contador_geracoes):
        """Método base para ser sobreescrito nas subclasses."""
        pass