from abc import ABCMeta, abstractmethod

class Populacao(metaclass=ABCMeta):
    @abstractmethod
    def gerar_populacao(self, populacao_atual):
        pass