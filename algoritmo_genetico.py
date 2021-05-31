import time


from cromossomo_utilidades import CromossomoUtilidades
from cruzamento_dois_pontos import CruzamentoDoisPontos
from cruzamento_uniforme import CruzamentoUniforme
from itens_mochila import ItensMochila
from geracao_utilidades import GeracaoUtilidades
from populacao_aleatoria import PopulacaoAleatoria
from populacao_elitismo import PopulacaoElitismo
from populacao_mu_lambda import PopulacaoMuLambda
from selecao_roleta import SelecaoRoleta
from selecao_torneio import SelecaoTorneio
from tendencia import Tendencia
import utilidades


# Constantes

ITENS_MOCHILA_CAMINHO_ARQUIVO = 'itens_mochila.csv'
ITENS_MOCHILA_SEPARADOR_DADOS = ';'
POPULACAO_QUANTIDADE_CROMOSSOMOS = 1000
POPULACAO_QUANTIDADE_GENES_CROMOSSOMO = 500
POPULACAO_POR_MU_LAMBDA = True
POPULACAO_ELITISMO_PERCENTUAL_SOBREVIVENTES = 10
MOCHILA_CAPACIDADE_MAXIMA = 12
CRUZAMENTO_UNIFORME_QUANTIDADE_GENES_POR_GRUPO = 1
CRUZAMENTO_UNIFORME = True
MUTACAO_PERCENTUAL_MAXIMO_GENES_ALTERADOS = 10
MUTACAO_PERCENTUAL_CHANGE_GENE_ALTERAR = 90
SELECAO_TORNEIO_QUANTIDADE_PARTICIPANTES = 5
SELECAO_POR_ROLETA = True
EXECUCAO_QUANTIDADE_REPETICOES = 1
EXECUCAO_QUANTIDADE_GERACOES_SEM_EVOLUCAO = 20
EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO = 10
EXECUCAO_SALVAR_GERACAO_COMPLETA = False
TENDENCIA_PERCENTUAL = 80
GERACAO_PREFIXO_MELHORES = 'melhores';
GERACAO_PREFIXO_GERACAO = 'geracao';


# Execução principal do algorítmo genético

quantidade_geracoes_sem_evolucao = 0
melhor_fitness_ultima_geracao = 0.0
melhor_fitness_geracao_atual = 0.0
percentual_mutacao = 0
percentual_cruzamento = 100
contador_geracoes = 0
contador_execucoes = 0
populacao = []
geracao = None
tempo_inicio = 0
tempo_gasto = 0
melhor_fitness = 0.0

mochila = ItensMochila(ITENS_MOCHILA_CAMINHO_ARQUIVO, ITENS_MOCHILA_SEPARADOR_DADOS)
itens_mochila = mochila.itens()
cromossomo_utilidades = CromossomoUtilidades(itens_mochila, MOCHILA_CAPACIDADE_MAXIMA, MUTACAO_PERCENTUAL_MAXIMO_GENES_ALTERADOS, MUTACAO_PERCENTUAL_CHANGE_GENE_ALTERAR, POPULACAO_QUANTIDADE_GENES_CROMOSSOMO)
gerador_primeira_populacao = PopulacaoAleatoria(itens_mochila, MOCHILA_CAPACIDADE_MAXIMA, POPULACAO_QUANTIDADE_CROMOSSOMOS, POPULACAO_QUANTIDADE_GENES_CROMOSSOMO, cromossomo_utilidades)
tendencia = Tendencia(TENDENCIA_PERCENTUAL)
geracao_utilidades = GeracaoUtilidades(ITENS_MOCHILA_SEPARADOR_DADOS, GERACAO_PREFIXO_MELHORES, GERACAO_PREFIXO_GERACAO, cromossomo_utilidades, MOCHILA_CAPACIDADE_MAXIMA, POPULACAO_QUANTIDADE_CROMOSSOMOS)

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

for i in range(EXECUCAO_QUANTIDADE_REPETICOES):
    contador_execucoes += 1

    tempo_inicio = time.time()

    populacao = gerador_primeira_populacao.gerar_populacao()
    geracao = geracao_utilidades.apurar_geracao(populacao)
    melhor_fitness = geracao['fitness'][0]
    contador_geracoes += 1
    geracao_utilidades.salvar_melhor(geracao, contador_execucoes)
    if EXECUCAO_SALVAR_GERACAO_COMPLETA:
        geracao_utilidades.salvar_geracao(geracao, contador_execucoes, contador_geracoes)
    tempo_gasto = time.time() - tempo_inicio
    utilidades.imprimir_informacoes(contador_geracoes, percentual_mutacao, percentual_cruzamento, tempo_gasto, quantidade_geracoes_sem_evolucao, melhor_fitness)

    while True:
        tempo_inicio = time.time()
        populacao = gerador_demais_populacoes.gerar_populacao(geracao['solucao'].tolist(), percentual_mutacao)
        geracao = geracao_utilidades.apurar_geracao(populacao)
        if melhor_fitness == geracao['fitness'][0]:
            if (100-percentual_mutacao) >= EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO:
                percentual_mutacao += EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO
            if percentual_cruzamento >= EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO:
                percentual_cruzamento -= EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO
            quantidade_geracoes_sem_evolucao += 1
        else:
            melhor_fitness = geracao['fitness'][0]
            if (100-percentual_cruzamento) >= EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO:
                percentual_cruzamento += EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO
            if percentual_mutacao >= EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO:
                percentual_mutacao -= EXECUCAO_PERCENTUAL_INCREMENTO_SEM_EVOLUCAO
            quantidade_geracoes_sem_evolucao = 0
        contador_geracoes += 1
        geracao_utilidades.salvar_melhor(geracao, contador_execucoes)
        if EXECUCAO_SALVAR_GERACAO_COMPLETA:
            geracao_utilidades.salvar_geracao(geracao, contador_execucoes, contador_geracoes)
        tempo_gasto = time.time() - tempo_inicio
        utilidades.imprimir_informacoes(contador_geracoes, percentual_mutacao, percentual_cruzamento, tempo_gasto, quantidade_geracoes_sem_evolucao, melhor_fitness)

        if quantidade_geracoes_sem_evolucao >= EXECUCAO_QUANTIDADE_GERACOES_SEM_EVOLUCAO:
            break

