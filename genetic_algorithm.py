import random
import math
import time
import pandas as pd

# Valores constantes
DATA_PATH = 'backpack.csv'
DATA_SEPARATOR = ';'
RESULTS_PATH = 'results.csv'
POPULATION_SIZE = 1000
WEIGHT_MAX = 12
CROSSOVER_SLICE_SIZE = 2
GENERATION_LENGTH = 20
COLUMN_ITEM_LABEL = 'item'
COLUMN_WEIGHT_LABEL = 'weight'
COLUMN_UTILITY_LABEL = 'utility'
COLUMN_PRICE_LABEL = 'price'
COLUMN_NONE_LABEL = 'none'
COLUMN_GOAL_LABEL = 'goal'
COLUMN_SOLUTION_LABEL = 'solution'
DATA_LABELS = [COLUMN_ITEM_LABEL, COLUMN_WEIGHT_LABEL,
               COLUMN_UTILITY_LABEL, COLUMN_PRICE_LABEL, COLUMN_NONE_LABEL]

# Variáveis globais

# Dados do arquivo CSV
raw_data = None

# Última população gerada
population = None

# Geração calculada, ou seja, a última população com o valor de fitness calculado
generation = None

# Array com os índices dos items que possuem tendência, ou seja,
# mais de 80% da população com o mesmo valor
tendency = []

# Melhor resultado de cada geração
bestests = pd.DataFrame(columns=[COLUMN_SOLUTION_LABEL, COLUMN_WEIGHT_LABEL,
                                 COLUMN_UTILITY_LABEL, COLUMN_PRICE_LABEL, COLUMN_GOAL_LABEL])


def load_file():
    """Carregamento do arquivo CSV através da biblioteca Pandas.

    Após o carregamento os itens são ordenados pela fôrmula: Utilidade / Preço.

    O caminho do arquivo é definido pela variável global DATA_PATH."""
    result = pd.read_csv(DATA_PATH, sep=DATA_SEPARATOR,
                         header=0, names=DATA_LABELS)
    result[COLUMN_WEIGHT_LABEL] = result[COLUMN_WEIGHT_LABEL].apply(
        lambda x: str(x).replace(',', '.')).astype(float)
    result[COLUMN_PRICE_LABEL] = result[COLUMN_PRICE_LABEL].apply(
        lambda x: str(x).replace(',', '.')).astype(float)
    result = result.drop(labels=COLUMN_NONE_LABEL, axis=1)
    result = result.loc[(result[COLUMN_UTILITY_LABEL] /
                         result[COLUMN_PRICE_LABEL]).sort_values().index]
    return result


def population_random(size):
    """Gera uma população totalmente aleatória, apenas respeitando a
    capacidade máxima atribuída na variável global WEIGHT_MAX.

    O tamanho da população é definido pela parâmetro SIZE."""
    global population
    for _ in range(size):
        current_weight = 0.0
        line = []
        for i in range(len(raw_data)):
            if ((current_weight + raw_data[COLUMN_WEIGHT_LABEL][i]) < WEIGHT_MAX) and (bool(random.getrandbits(1)) == True):
                line.append(1)
                current_weight += raw_data[COLUMN_WEIGHT_LABEL][i]
            else:
                line.append(0)
        population.append(line)


def population_next(crossover_rate):
    """Gera a população próxima do algoritmo utilizando os seguintes critérios:

    Mantém o 1% melhor da população anterior;

    Realiza um cruzamento (crossover) entre o 1% melhor;

    O restante da população desta função é gerada através do cruzamento entre
    duas soluções escolhidas aleatóriamente, o valor total de indivíduos é definido
    pelo parâmetro CROSSOVER_RATE.

    Em cada etapa a capacidade máxima atribuída da variável global WEIGHT_MAX é respeitada."""
    global population
    global generation
    for i in range(math.ceil(POPULATION_SIZE*0.01)):
        for j in range(math.ceil(POPULATION_SIZE*0.01)):
            if i == j:
                population.append(generation[COLUMN_SOLUTION_LABEL][i])
            else:
                population.append(
                    crossover(generation[COLUMN_SOLUTION_LABEL][i], generation[COLUMN_SOLUTION_LABEL][j]))
    for _ in range(math.ceil(POPULATION_SIZE*crossover_rate/100)):
        mother_index = calculate_index_by_random_value(
            random.randint(0, calculate_max_value()-1))
        father_index = calculate_index_by_random_value(
            random.randint(0, calculate_max_value()-1))
        population.append(
            crossover(generation[COLUMN_SOLUTION_LABEL][mother_index], generation[COLUMN_SOLUTION_LABEL][father_index]))
    if len(population) < 500:
        for _ in range(500-len(population)):
            index = calculate_index_by_random_value(
                random.randint(0, calculate_max_value()-1))
            population.append(generation[COLUMN_SOLUTION_LABEL][index])


def population_mutation(mutation_rate=5):
    """Realiza uma mutação aleatória em um percetual da
    população definido pelo parâmetro MUTATION_RATE."""
    population_current_size = len(population)
    for _ in range(math.floor(population_current_size*mutation_rate/100)):
        multation_index = random.randint(math.floor(
            population_current_size*(100-mutation_rate)/100), population_current_size-1)
        population[multation_index] = multation(population[multation_index])


def calculate_goal(item):
    """Calcula o fitness de um possível solução."""
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


def calculate_tendency():
    """Calcula a tendência de um item na população e
    guarda os indeces destes itens."""
    global tendency
    tendency = pd.DataFrame(pd.DataFrame(population).mean(), columns=['mean'])
    tendency_minimum = math.floor(len(population)*0.2)/len(population)
    tendency_maximum = math.floor(len(population)*0.8)/len(population)
    tendency = tendency[(tendency['mean'] < tendency_minimum)
                        | (tendency['mean'] > tendency_maximum)].index.tolist()


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
    """Verifica os indices com tendência e altera os valores deles.

    Realiza uma mutação em 10% dos valores.

    A mutação segue respeitando a capacidade máxima (WEIGHT_MAX)."""
    result = item.copy()

    for i in tendency:
        result[i] = 0 if result[i] == 1 else 1

    current_weight = calculate_weight(result)
    multation_count = 0
    while multation_count < math.floor(len(raw_data)*0.1):
        i = random.randint(0, len(raw_data)-1)
        if result[i] == 1:
            result[i] = 0
            current_weight -= raw_data[COLUMN_WEIGHT_LABEL][i]
            if current_weight < 12:
                multation_count += 1
        elif (current_weight + raw_data[COLUMN_WEIGHT_LABEL][i]) < WEIGHT_MAX:
            result[i] = 1
            current_weight += raw_data[COLUMN_WEIGHT_LABEL][i]
            multation_count += 1
    return result


def generation_save_best():
    """Salva a melhor solução em um arquivo CSV, cujo caminho
    é definido pela variável RESULTS_PATH."""
    global bestests
    bestests.loc[bestests.shape[0]] = generation.loc[0]
    bestests.to_csv(RESULTS_PATH, sep=DATA_SEPARATOR, index=False)


def generation_info(generation_count, mutation_rate, crossorver_rate, execution_time, evolution_freezed_for, generation_best):
    """Imprime no console alguns dados da geração atual."""
    print('generation: {}'.format(generation_count))
    print('took: {}s'.format(execution_time))
    print('mutation rate of: {}%'.format(mutation_rate))
    print('crossover rate of: {}%'.format(crossorver_rate))
    print('evolution freezed for: {}'.format(evolution_freezed_for))
    print('best: {}'.format(generation_best))
    print('------------------------------------------------')


def genetic_algorithm():
    """Execução do algoritmo genético.

    A quantidade de gerações é definida pela variável global GENERATION_LENGTH e
    a taxa de mutação tenha atingido seu valor máximo. Quando ambos forem verdadeiro
    a execução é interrompida.
    """

    global population

    # Quantidade de gerações que não há evolução
    evolution_freezed_for = 1
    # Melhor valor da última geração
    generation_last_best = 0
    # Taxa de mutação
    mutation_rate = 5
    # Taxa de cruzamento
    crossorver_rate = 80
    # Contador de gerações
    generation_count = 1
    # Horário inicial
    start_time = time.time()

    population = []
    population_random(POPULATION_SIZE)
    fitness()
    generation_save_best()
    generation_info(generation_count, mutation_rate, crossorver_rate, time.time(
    ) - start_time, evolution_freezed_for, generation[COLUMN_GOAL_LABEL][0])
    generation_count += 1

    while True:
        population = []
        population_next(crossorver_rate)
        population_random(POPULATION_SIZE-len(population))
        calculate_tendency()
        population_mutation(mutation_rate)
        fitness()
        generation_save_best()
        generation_info(generation_count, mutation_rate, crossorver_rate, time.time(
        ) - start_time, evolution_freezed_for, generation[COLUMN_GOAL_LABEL][0])
        if (generation[COLUMN_GOAL_LABEL][0] == generation_last_best):
            evolution_freezed_for += 1
            if (mutation_rate < 80):
                mutation_rate += 5
            if (crossorver_rate > 5):
                crossorver_rate -= 5
        else:
            generation_last_best = generation[COLUMN_GOAL_LABEL][0]
            evolution_freezed_for = 1
            if (mutation_rate > 5):
                mutation_rate -= 5
            if (crossorver_rate < 80):
                crossorver_rate += 5
        if (GENERATION_LENGTH <= evolution_freezed_for) and (mutation_rate > 70):
            break
        else:
            generation_count += 1
        start_time = time.time()


# Entrada execução do arquivo.
raw_data = load_file()
genetic_algorithm()
