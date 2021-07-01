import math
import random


def sorteio_premiado(percentual_premiacao):
    """Método para realização de sorteios aleatórios onde retorna True se o valor sorteado
    está dentro do percentual passado ou False senão."""
    valor_sorteado = random.randint(1, 100)
    return valor_sorteado <= percentual_premiacao


def imprimir_informacoes(contador_geracoes, taxa_mutacao, tempo_execucao, quantidade_geracoes_sem_evolucao, melhor_fitness):
    """Imprime os dados no console."""
    print('Geração: {}'.format(contador_geracoes))
    print('Tempo gasto: {}s'.format(math.ceil(tempo_execucao)))
    print('Taxa de Mutação: {}%'.format(taxa_mutacao))
    print('Quantidade de Gerações sem Evolução: {}'.format(quantidade_geracoes_sem_evolucao))
    if not(melhor_fitness) == None:
        print('Melhor Fitness da Geração: {}'.format(melhor_fitness))
    print('------------------------------------------------')