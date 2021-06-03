from abc import ABCMeta, abstractmethod

class Selecao(metaclass=ABCMeta):
    """Classe base para implementação das técnicas de seleção de cromossomo."""

    @abstractmethod
    def selecionar_cromossomo(self, populacao):
        """Método base para ser sobreescrito nas subclasses."""
        pass