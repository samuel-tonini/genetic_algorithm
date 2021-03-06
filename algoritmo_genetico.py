import time


from cromossomo_utilidades import CromossomoUtilidades
from cruzamento_dois_pontos import CruzamentoDoisPontos
from cruzamento_uniforme import CruzamentoUniforme
from itens_mochila import ItensMochila
from geracao_utilidades import GeracaoUtilidades
from ordenacao_multiobjetivo import OrdenacaoMultiobjetivo
from ordenacao_simples import OrdenacaoSimples
from populacao_aleatoria import PopulacaoAleatoria
from populacao_elitismo import PopulacaoElitismo
from populacao_mu_lambda import PopulacaoMuLambda
from populacao_preencher import PopulacaoPreencher
from selecao_roleta import SelecaoRoleta
from selecao_torneio import SelecaoTorneio
from tendencia_por_esquemas import TendenciaPorEsquemas
from tendencia_por_quantidade import TendenciaPorQuantidade
import utilidades


# Constantes

ITENS_MOCHILA_CAMINHO_ARQUIVO = 'itens_mochila.csv'
ITENS_MOCHILA_SEPARADOR_DADOS = ';'
POPULACAO_QUANTIDADE_CROMOSSOMOS = 1000
POPULACAO_QUANTIDADE_GENES_CROMOSSOMO = 500
POPULACAO_ELITISMO_PERCENTUAL_SOBREVIVENTES = 10
MOCHILA_CAPACIDADE_MAXIMA = 12
CRUZAMENTO_UNIFORME_QUANTIDADE_GENES_POR_GRUPO = 1
MUTACAO_PERCENTUAL_MAXIMO_GENES_ALTERADOS = 10
MUTACAO_PERCENTUAL_CHANGE_GENE_ALTERAR = 5
SELECAO_TORNEIO_QUANTIDADE_PARTICIPANTES = 5
EXECUCAO_QUANTIDADE_GERACOES_SEM_EVOLUCAO = 20
EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO = 10
TENDENCIA_PERCENTUAL = 80
GERACAO_PREFIXO_MELHORES = 'melhores';
GERACAO_PREFIXO_MELHORES_MULTIOBJETIVO = 'melhores_multiobjetivo';
GERACAO_PREFIXO_GERACAO = 'geracao';

# Variáveis controle algoritmo

# True = Salva toda a geração
# False = Salva apenas os melhores
EXECUCAO_SALVAR_GERACAO_COMPLETA = False

# True = População por Mu Lambda
# False = População por Elitismo
POPULACAO_POR_MU_LAMBDA = True

# True = Cruzamento Uniforme
# False = Cruzamento Dois Pontos
CRUZAMENTO_UNIFORME = True

# True = Seleção por Roleta
# False = Seleção por Torneio
SELECAO_POR_ROLETA = True

# Quantidade de repetições que a configuração atual será executada
EXECUCAO_QUANTIDADE_REPETICOES = 1

# True = Tendência por Quantidade
# False = Tendência por Esquemas
TEDENCIA_POR_QUANTIDADE = False

# Quantidade mínina de esquemas para que a população não seja classificada como tendenciosa
TENDENCIA_QUANTIDADE_MINIMA_ESQUEMAS = 10

# Quantidade máxima de cromossomos em um grupo para que a população seja classificada como tendenciosa
TENDENCIA_GRUPO_QUANTIDADE_MAXIMA_CROMOSSOMOS = 100

# Distância máxima para um cromossomo entrar em um grupo já existente
TENDENCIA_GRUPO_DISTANCIA = 10

# Frequência de execução do método de tendência
TENDENCIA_FREQUENCIA_EXECUCAO = 1

# Matriz de jugamento método AHP
AHP_MATRIZ_JULGAMENTO = { 'utilidade': { 'preco': 1/5, 'peso': 1/9 }, 'peso': { 'preco': 9 } }

# Se utiliza o multiobjetivo ou não, utilizando apenas utilidade / preço
MULTIOBJETIVO = True

# Tecnica de ordenação multiobjetivo
# AHP = True
# Borda = False
MULTIOBJETIVO_AHP = True

# Quantidade máxima de gerações do algoritmo
EXECUCAO_QUANTIDADE_GERACOES_MAXIMA = 100


# Execução principal do algoritmo genético

mochila = ItensMochila(ITENS_MOCHILA_CAMINHO_ARQUIVO, ITENS_MOCHILA_SEPARADOR_DADOS)
itens_mochila = mochila.itens()
cromossomo_utilidades = CromossomoUtilidades(itens_mochila, MOCHILA_CAPACIDADE_MAXIMA, MUTACAO_PERCENTUAL_MAXIMO_GENES_ALTERADOS, MUTACAO_PERCENTUAL_CHANGE_GENE_ALTERAR, POPULACAO_QUANTIDADE_GENES_CROMOSSOMO)
gerador_primeira_populacao = PopulacaoAleatoria(itens_mochila, MOCHILA_CAPACIDADE_MAXIMA, POPULACAO_QUANTIDADE_CROMOSSOMOS, POPULACAO_QUANTIDADE_GENES_CROMOSSOMO, cromossomo_utilidades)
geracao_utilidades = GeracaoUtilidades(ITENS_MOCHILA_SEPARADOR_DADOS, GERACAO_PREFIXO_MELHORES, GERACAO_PREFIXO_GERACAO, cromossomo_utilidades, MOCHILA_CAPACIDADE_MAXIMA, POPULACAO_QUANTIDADE_CROMOSSOMOS, MULTIOBJETIVO, GERACAO_PREFIXO_MELHORES_MULTIOBJETIVO)

if TEDENCIA_POR_QUANTIDADE:
    tendencia = TendenciaPorQuantidade(TENDENCIA_FREQUENCIA_EXECUCAO, TENDENCIA_PERCENTUAL)
else:
    tendencia = TendenciaPorEsquemas(TENDENCIA_FREQUENCIA_EXECUCAO, TENDENCIA_QUANTIDADE_MINIMA_ESQUEMAS, TENDENCIA_GRUPO_DISTANCIA, TENDENCIA_GRUPO_QUANTIDADE_MAXIMA_CROMOSSOMOS, POPULACAO_QUANTIDADE_GENES_CROMOSSOMO)

if CRUZAMENTO_UNIFORME:
    tecnica_cruzamento = CruzamentoUniforme(POPULACAO_QUANTIDADE_GENES_CROMOSSOMO, CRUZAMENTO_UNIFORME_QUANTIDADE_GENES_POR_GRUPO, cromossomo_utilidades)
else:
    tecnica_cruzamento = CruzamentoDoisPontos(POPULACAO_QUANTIDADE_GENES_CROMOSSOMO, cromossomo_utilidades)

if SELECAO_POR_ROLETA:
    metodo_selecao = SelecaoRoleta()
else:
    metodo_selecao = SelecaoTorneio(SELECAO_TORNEIO_QUANTIDADE_PARTICIPANTES)

if POPULACAO_POR_MU_LAMBDA:
    gerador_demais_populacoes = PopulacaoMuLambda(POPULACAO_QUANTIDADE_CROMOSSOMOS, tecnica_cruzamento, cromossomo_utilidades, metodo_selecao, tendencia)
else:
    gerador_demais_populacoes = PopulacaoElitismo(POPULACAO_QUANTIDADE_CROMOSSOMOS, POPULACAO_ELITISMO_PERCENTUAL_SOBREVIVENTES, tecnica_cruzamento, cromossomo_utilidades, metodo_selecao, tendencia)

if MULTIOBJETIVO:
    ordenacao = OrdenacaoMultiobjetivo(cromossomo_utilidades, MOCHILA_CAPACIDADE_MAXIMA, POPULACAO_QUANTIDADE_CROMOSSOMOS)
else:
    ordenacao = OrdenacaoSimples(cromossomo_utilidades, MOCHILA_CAPACIDADE_MAXIMA, POPULACAO_QUANTIDADE_CROMOSSOMOS)


populacao_preenchimento = PopulacaoPreencher(POPULACAO_QUANTIDADE_CROMOSSOMOS, tecnica_cruzamento, cromossomo_utilidades, metodo_selecao)

contador_execucoes = 0

for i in range(EXECUCAO_QUANTIDADE_REPETICOES):
    quantidade_geracoes_sem_evolucao = 0
    melhor_fitness_ultima_geracao = 0.0
    melhor_fitness_geracao_atual = 0.0
    percentual_mutacao = 0
    contador_geracoes = 0
    populacao = []
    geracao = None
    tempo_inicio = 0
    tempo_gasto = 0
    melhor_fitness = 0.0

    contador_execucoes += 1

    tempo_inicio = time.time()

    populacao = gerador_primeira_populacao.gerar_populacao()
    geracao = ordenacao.ordenar_populacao(populacao)
    if MULTIOBJETIVO:
        melhor_fitness = geracao['utilidade'][0] + geracao['preco'][0] + geracao['peso'][0]
    else:
        melhor_fitness = geracao['fitness'][0]
    contador_geracoes += 1
    geracao_utilidades.salvar_melhor(geracao, contador_execucoes)
    if EXECUCAO_SALVAR_GERACAO_COMPLETA:
        geracao_utilidades.salvar_geracao(geracao, contador_execucoes, contador_geracoes)
    tempo_gasto = time.time() - tempo_inicio
    if MULTIOBJETIVO:
        utilidades.imprimir_informacoes(contador_geracoes, percentual_mutacao, tempo_gasto, quantidade_geracoes_sem_evolucao, None)
    else:
        utilidades.imprimir_informacoes(contador_geracoes, percentual_mutacao, tempo_gasto, quantidade_geracoes_sem_evolucao, melhor_fitness)

    while contador_geracoes <= EXECUCAO_QUANTIDADE_GERACOES_MAXIMA:
        tempo_inicio = time.time()
        geracao = geracao_utilidades.remover_duplicados(geracao)
        populacao = populacao_preenchimento.gerar_populacao(geracao['solucao'].tolist())
        populacao = gerador_demais_populacoes.gerar_populacao(geracao['solucao'].tolist(), percentual_mutacao, contador_geracoes)
        geracao = ordenacao.ordenar_populacao(populacao)
        if MULTIOBJETIVO:
            melhor_atual = geracao['utilidade'][0] + geracao['preco'][0] + geracao['peso'][0]
        else:
            melhor_atual = geracao['fitness'][0]
        if melhor_fitness == melhor_atual:
            if (100-percentual_mutacao) >= EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO:
                percentual_mutacao += EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO
            quantidade_geracoes_sem_evolucao += 1
        else:
            melhor_fitness = melhor_atual
            if percentual_mutacao >= EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO:
                percentual_mutacao -= EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO
            quantidade_geracoes_sem_evolucao = 0
        contador_geracoes += 1
        geracao_utilidades.salvar_melhor(geracao, contador_execucoes)
        if EXECUCAO_SALVAR_GERACAO_COMPLETA:
            geracao_utilidades.salvar_geracao(geracao, contador_execucoes, contador_geracoes)
        tempo_gasto = time.time() - tempo_inicio
        if MULTIOBJETIVO:
            utilidades.imprimir_informacoes(contador_geracoes, percentual_mutacao, tempo_gasto, quantidade_geracoes_sem_evolucao, None)
        else:
            utilidades.imprimir_informacoes(contador_geracoes, percentual_mutacao, tempo_gasto, quantidade_geracoes_sem_evolucao, melhor_fitness)

        if quantidade_geracoes_sem_evolucao >= EXECUCAO_QUANTIDADE_GERACOES_SEM_EVOLUCAO:
            break

    if MULTIOBJETIVO:
        geracao = geracao[geracao['fitness']==0]
        geracao = geracao_utilidades.calcular_ahp(geracao, AHP_MATRIZ_JULGAMENTO)
        geracao = geracao_utilidades.calcular_borda(geracao)
        geracao_utilidades.salvar_melhores_multiobjetivo(geracao, contador_execucoes)

