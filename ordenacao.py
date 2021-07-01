from abc import ABCMeta, abstractmethod

class Ordenacao(metaclass=ABCMeta):
    """Classe base para implementação das técnicas de ordenação da população."""

    @abstractmethod
    def ordenar_populacao(self, populacao):
        """Método base para ser sobreescrito nas subclasses."""
        pass