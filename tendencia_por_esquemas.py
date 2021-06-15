class TendenciaPorEsquemas:
    """Classe com a implementação da técnica de quebra de tendência dos genes."""

    def __init__(self, frequencia_execucao, quantidade_minima_grupos, distancia_maxima_entre_cromossomos, quantida_maxima_elementos_grupo, quantidade_genes_por_cromossomo):
        """Parâmetros:

        frequencia_execucao = Quantidade de geraçÕes que serão aguardadas para uma nova execução;

        quantidade_minima_grupos = Quantidade mínima de grupos para indicar que não há convergência da população;

        distancia_maxima_entre_cromossomos = Quantidade máxima de genes que poderão ser diferentes e o cromossomo ainda
        pertenserá a um grupo mesmo que não seja exatamente igual;

        quantida_maxima_elementos_grupo = Quantidade máxima de cromossomos no grupo para indicar que há convergência
        da população;

        quantidade_genes_por_cromossomo = Total de genes por cromossomo."""
        self.frequencia_execucao = frequencia_execucao
        self.__quantidade_minima_grupos = quantidade_minima_grupos
        self.__distancia_maxima_entre_cromossomos = distancia_maxima_entre_cromossomos
        self.__quantida_maxima_elementos_grupo = quantida_maxima_elementos_grupo
        self.__quantidade_genes_por_cromossomo = quantidade_genes_por_cromossomo
    
    def calcular_indices_tendenciosos(self, populacao):
        """Calcula os índices tedenciosos para que as mutações ocorram nestes índices, gerando assim
        uma população com uma diversidade maior."""
        grupos = []
        resultado = []
        for cromossomo in populacao:
            if len(grupos) > self.__quantidade_minima_grupos:
                return []
            elif len(grupos) == 0:
                grupos.append([cromossomo, 1])
            else:
                for elemento in grupos:
                    distancia = 0
                    for indice_gene in range(self.__quantidade_genes_por_cromossomo):
                        if elemento[0][indice_gene] != cromossomo[indice_gene]:
                            distancia += 1
                    if distancia > self.__distancia_maxima_entre_cromossomos:
                        grupos.append([cromossomo, 1])
                        break
                    else:
                        elemento[1] += 1
        for elemento in grupos:
            if elemento[1] > self.__quantida_maxima_elementos_grupo:
                for indice_gene in range(self.__quantidade_genes_por_cromossomo):
                    if elemento[0][indice_gene] == 1:
                        resultado.append(indice_gene)
        return list(set(resultado))
