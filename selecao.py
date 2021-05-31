from abc import ABCMeta, abstractmethod

class Selecao(metaclass=ABCMeta):
    @abstractmethod
    def selecionar_cromossomo(self, populacao):
        pass