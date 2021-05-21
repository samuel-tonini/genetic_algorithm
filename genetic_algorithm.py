import random
import math
import pandas as pd
import numpy as np

# Valores constantes
DATA_PATH = 'backpack.csv'
DATA_SEPARATOR = ';'
POPULATION_SIZE = 1000
WEIGHT_MAX = 12
CROSSOVER_SLICE_SIZE = 5
GENERATION_LENGTH = 30
COLUMN_ITEM_LABEL = 'item'
COLUMN_WEIGHT_LABEL = 'weight'
COLUMN_UTILITY_LABEL = 'utility'
COLUMN_PRICE_LABEL = 'price'
COLUMN_NONE_LABEL = 'none'
COLUMN_GOAL_LABEL = 'goal'
COLUMN_SOLUTION_LABEL = 'solution'
DATA_LABELS = [COLUMN_ITEM_LABEL, COLUMN_WEIGHT_LABEL,
               COLUMN_UTILITY_LABEL, COLUMN_PRICE_LABEL, COLUMN_NONE_LABEL]
GENETIC_ALGORITHM_PRINT_SIZE = 1

# Variáveis globais

"""Dados do arquivo CSV."""
raw_data = None

"""Última população gerada."""
population = None

"""Geração calculada."""
generation = None


def load_file():
    """Carregamento do arquivo CSV através da biblioteca Pandas.

    O caminho do arquivo é definido pela variável global DATA_PATH.
    """
    result = pd.read_csv(DATA_PATH, sep=DATA_SEPARATOR,
                         header=0, names=DATA_LABELS)
    result[COLUMN_WEIGHT_LABEL] = result[COLUMN_WEIGHT_LABEL].apply(
        lambda x: str(x).replace(',', '.')).astype(float)
    result[COLUMN_PRICE_LABEL] = result[COLUMN_PRICE_LABEL].apply(
        lambda x: str(x).replace(',', '.')).astype(float)
    result = result.drop(labels=COLUMN_NONE_LABEL, axis=1)
    return result


def population_initial():
    """Gera a população inicial do algoritmo totalmente aleatória,
    apenas respeitando a capacidade máxima atribuída na variável global WEIGHT_MAX.

    O tamanho da população é definido pela variável global POPULATION_SIZE.
    """
    global population
    population = []
    for _ in range(POPULATION_SIZE):
        current_weight = 0.0
        line = []
        for i in range(len(raw_data)):
            if ((current_weight + raw_data[COLUMN_WEIGHT_LABEL][i]) < WEIGHT_MAX) and (bool(random.getrandbits(1)) == True):
                line.append(1)
                current_weight += raw_data[COLUMN_WEIGHT_LABEL][i]
            else:
                line.append(0)
        population.append(line)


def population_next():
    """Gera a população próxima do algoritmo utilizando os seguintes critérios:

    Mantém o 1% melhor da população anterior;

    Realiza um cruzamento (crossover) entre o 1% melhor;

    O restante da população é gerada através do método roleta.

    Em cada etapa a capacidade máxima atribuída da variável global WEIGHT_MAX é respeitada.

    O tamanho da população é definido pela variável global POPULATION_SIZE.
    """
    global population
    global generation
    population = []
    for i in range(math.ceil(POPULATION_SIZE*0.01)):
        for j in range(math.ceil(POPULATION_SIZE*0.01)):
            if i == j:
                population.append(generation[COLUMN_SOLUTION_LABEL][i])
            else:
                population.append(
                    crossover(generation[COLUMN_SOLUTION_LABEL][i], generation[COLUMN_SOLUTION_LABEL][j]))
    for _ in range(POPULATION_SIZE-len(population)):
        mother_index = calculate_index_by_random_value(
            random.randint(0, calculate_max_value()-1))
        father_index = calculate_index_by_random_value(
            random.randint(0, calculate_max_value()-1))
        population.append(
            crossover(generation[COLUMN_SOLUTION_LABEL][mother_index], generation[COLUMN_SOLUTION_LABEL][father_index]))


def population_mutation():
    """Realiza uma mutação aleatória em 5% da população."""
    for i in range(math.floor(POPULATION_SIZE*0.05)):
        multation_index = random.randint(0, POPULATION_SIZE-1)
        population[multation_index] = multation(
            population[multation_index])


def calculate_goal(item):
    """Calcula o objetivo de um possível solução."""
    total = []
    for i in range(len(item)):
        if item[i] == 1:
            total.append(raw_data[COLUMN_UTILITY_LABEL][i] /
                         raw_data[COLUMN_PRICE_LABEL][i])
    return sum(total)


def calculate_weight(item):
    """Calcula o peso de um possível solução."""
    total = []
    for i in range(len(item)):
        if item[i] == 1:
            total.append(raw_data[COLUMN_WEIGHT_LABEL][i])
    return sum(total)


def calculate_price(item):
    """Calcula o preço de um possível solução."""
    total = []
    for i in range(len(item)):
        if item[i] == 1:
            total.append(raw_data[COLUMN_PRICE_LABEL][i])
    return sum(total)


def calculate_utility(item):
    """Calcula o utilidade de um possível solução."""
    total = []
    for i in range(len(item)):
        if item[i] == 1:
            total.append(raw_data[COLUMN_UTILITY_LABEL][i])
    return sum(total)


def fitness():
    """Gera um Pandas.DataFrame contendo as possíveis soluções, seus pesos, utilidades,
    preços e objetivos.

    Ordenado pela melhor solução e filtrando pela capacidade máxima."""
    global generation
    generation = pd.DataFrame(columns=[COLUMN_SOLUTION_LABEL, COLUMN_WEIGHT_LABEL,
                                       COLUMN_UTILITY_LABEL, COLUMN_PRICE_LABEL, COLUMN_GOAL_LABEL])
    for i in range(len(population)):
        line = population[i]
        generation.loc[i] = [line, calculate_weight(line), calculate_utility(
            line), calculate_price(line), calculate_goal(line)]
    generation = generation[generation[COLUMN_WEIGHT_LABEL]
                            <= WEIGHT_MAX].sort_values(COLUMN_GOAL_LABEL, ascending=False).reset_index(drop=True)


def calculate_max_value():
    """Calcula a soma dos primeiros N números naturais.

    Onde N é o tamanho da população."""
    return (POPULATION_SIZE+1)*POPULATION_SIZE/2


def calculate_index_by_random_value(random_value):
    """Calcula um índice para realizar o cruzamento, baseando-se em um valor
    aleatório.

    O cálculo é realizado descrobrindo quantos N primeiros números naturais
    devem ser somados para atingir esse valor."""
    a = 1
    b = 1
    c = random_value * 2 * -1
    sol_1 = (-b - math.sqrt(b**2 - 4*a*c)) / (2 * a)
    sol_2 = (-b + math.sqrt(b**2 - 4*a*c)) / (2 * a)
    if not sol_1.is_integer():
        sol_1 = math.ceil(sol_1)
    if not sol_2.is_integer():
        sol_2 = math.ceil(sol_2)
    if sol_1 > 0:
        return int(POPULATION_SIZE - sol_1)
    elif sol_2 > 0:
        return int(POPULATION_SIZE - sol_2)
    else:
        return 0


def crossover(mother, father):
    """Realiza o cruzamento entre duas possíveis soluções utilizando uma fatia definida
    na variável global CROSSOVER_SLICE_SIZE.

    O cruzamento segue respeitando a capacidade máxima (WEIGHT_MAX)."""
    current_weight = 0.0
    result = []
    for i in range(math.floor(len(raw_data)/CROSSOVER_SLICE_SIZE)):
        origin = mother if random.getrandbits(1) == True else father
        for j in range(CROSSOVER_SLICE_SIZE):
            index = i*CROSSOVER_SLICE_SIZE+j
            if (current_weight + raw_data[COLUMN_WEIGHT_LABEL][index]) < WEIGHT_MAX:
                result.append(origin[index])
                if origin[index] == 1:
                    current_weight += raw_data[COLUMN_WEIGHT_LABEL][index]
            else:
                result.append(0)
    if len(result) < len(raw_data):
        for i in range(len(raw_data) - len(result)):
            if (current_weight + raw_data[COLUMN_WEIGHT_LABEL][i]) < WEIGHT_MAX:
                result.append(1)
            else:
                result.append(0)
    return result


def multation(item):
    """Realiza uma mutação em 1% dos valores.

    A mutação segue respeitando a capacidade máxima (WEIGHT_MAX)."""
    result = item.copy()
    current_weight = calculate_weight(item)
    multation_count = 0
    while multation_count < math.floor(len(raw_data)*0.1):
        i = random.randint(0, len(raw_data)-1)
        if result[i] == 1:
            result[i] = 0
            current_weight -= raw_data[COLUMN_WEIGHT_LABEL][i]
            multation_count += 1
        elif (current_weight + raw_data[COLUMN_WEIGHT_LABEL][i]) < WEIGHT_MAX:
            result[i] = 1
            current_weight += raw_data[COLUMN_WEIGHT_LABEL][i]
            multation_count += 1
    return result


def genetic_algorithm():
    """Execução do algoritmo genético.

    A quantidade de gerações é definida pela variável global GENERATION_LENGTH.
    """
    population_initial()
    fitness()
    print('top {} of generation: 0'.format(GENETIC_ALGORITHM_PRINT_SIZE))
    print(generation.head(GENETIC_ALGORITHM_PRINT_SIZE))
    print('')
    print('')

    for i in range(GENERATION_LENGTH-1):
        population_next()
        population_mutation()
        fitness()
        print('top {} of generation: {}'.format(
            GENETIC_ALGORITHM_PRINT_SIZE, i+1))
        print(generation.head(GENETIC_ALGORITHM_PRINT_SIZE))
        print('')
        print('')


"""Entrada execução do arquivo.

Carrega o arquivo CSV e executa o algoritmo genético.
"""
raw_data = load_file()
genetic_algorithm()
