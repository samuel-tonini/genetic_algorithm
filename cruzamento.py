from abc import ABCMeta, abstractmethod

class Cruzamento(metaclass=ABCMeta):
    @abstractmethod
    def realizar_cruzamento(self, cromossomo_pai, cromossomo_mae):
        pass
