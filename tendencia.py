from abc import ABCMeta, abstractmethod


class Tendencia(metaclass=ABCMeta):
    """Classe base para implementação das técnicas de tendência da população."""

    @abstractmethod
    def calcular_indices_tendenciosos(self, populacao):
        """Método base para ser sobreescrito nas subclasses."""
        pass