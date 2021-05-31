import math
import random


def sorteio_premiado(percentual_premiacao):
    valor_sorteado = random.randint(1, 100)
    return valor_sorteado <= percentual_premiacao


def imprimir_informacoes(contador_geracoes, taxa_mutacao, taxa_cruzamento, tempo_execucao, quantidade_geracoes_sem_evolucao, melhor_fitness):
    print('Geração: {}'.format(contador_geracoes))
    print('Tempo gasto: {}s'.format(math.ceil(tempo_execucao)))
    print('Taxa de Mutação: {}%'.format(taxa_mutacao))
    print('Taxa Cruzamento: {}%'.format(taxa_cruzamento))
    print('Quantidade de Gerações sem Evolução: {}'.format(quantidade_geracoes_sem_evolucao))
    print('Melhor Fitness da Geração: {}'.format(melhor_fitness))
    print('------------------------------------------------')