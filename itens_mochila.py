import pandas as pd

class ItensMochila:
    def __init__(self, caminho_arquivo, separador_dados):
        self.__itens = pd.read_csv(caminho_arquivo, sep=separador_dados, header=0, names=['item', 'peso', 'utilidade', 'preco', 'nenhum'])
        for rotulo_coluna_decimal in ['peso', 'preco']:
            self.__itens[rotulo_coluna_decimal] = self.__itens[rotulo_coluna_decimal].apply(lambda x: str(x).replace(',', '.')).astype(float)
        self.__itens = self.__itens.drop(labels='nenhum', axis=1)


    def itens(self):
        return self.__itens


    def peso_por_indice(self, indice_item):
        return self.__itens['peso'][indice_item]


    def utilidade_por_indice(self, indice_item):
        return self.__itens['utilidade'][indice_item]


    def preco_por_indice(self, indice_item):
        return self.__itens['preco'][indice_item]


    def fitness_por_indice(self, indice_item):
        return utilidade_por_indice(indice_item) / preco_por_indice(indice_item)
