import pandas as pd

class ItensMochila:
    """Classe para manipular os dados do arquivo CSV."""

    def __init__(self, caminho_arquivo, separador_dados):
        """Parâmetros:

        caminho_arquivo = Caminho do arquivo CSV;

        separador_dados = Caracter para separação dos dados no arquivo."""
        self.__itens = pd.read_csv(caminho_arquivo, sep=separador_dados, header=0, names=['item', 'peso', 'utilidade', 'preco', 'nenhum'])
        for rotulo_coluna_decimal in ['peso', 'preco']:
            self.__itens[rotulo_coluna_decimal] = self.__itens[rotulo_coluna_decimal].apply(lambda x: str(x).replace(',', '.')).astype(float)
        self.__itens = self.__itens.drop(labels='nenhum', axis=1)


    def itens(self):
        """Método que retorna os itens do arquivo dentro de um dataframe."""
        return self.__itens


    def peso_por_indice(self, indice_item):
        """Retorna o peso de um item do arquivo, baseando em seu índice."""
        return self.__itens['peso'][indice_item]


    def utilidade_por_indice(self, indice_item):
        """Retorna a utilidade de um item do arquivo, baseando em seu índice."""
        return self.__itens['utilidade'][indice_item]


    def preco_por_indice(self, indice_item):
        """Retorna o preço de um item do arquivo, baseando em seu índice."""
        return self.__itens['preco'][indice_item]


    def fitness_por_indice(self, indice_item):
        """Calcula e retorna o fitness de um item do arquivo, baseando em seu índice."""
        return utilidade_por_indice(indice_item) / preco_por_indice(indice_item)
