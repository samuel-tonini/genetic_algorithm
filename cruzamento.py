from abc import ABCMeta, abstractmethod

class Cruzamento(metaclass=ABCMeta):
    """Classe base para a implementação das técnicas de cruzamento."""

    @abstractmethod
    def realizar_cruzamento(self, cromossomo_pai, cromossomo_mae):
        """Método base para ser sobreescrito nas subclasses."""
        pass
