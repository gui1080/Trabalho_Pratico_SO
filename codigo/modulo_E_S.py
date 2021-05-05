import numpy as np
import sys


def gerencia_de_entrada_saida():

    # pega o arquivo do terminal
    arquivo = sys.argv[2]

    # cria uma lista com o que foi lido do arquivo
    input = []
    with open(arquivo, 'r') as f:
        for line in f:
            input.append(int(line))

    f.close()

    # inicializa a lista de requisitos para cada algoritmo
    requisitions_SCAN = input.copy()
    last_cilinder = input.pop(0)
    requisitions_SSF = input.copy()
    actual_cilinder = input.pop(0)
    requisitions = input.copy()
    requisitions_SCAN.append(0)

    # ordena a lista de requisitos para os algoritmos SSF e SCAN
    requisitions_SSF.sort()
    requisitions_SCAN.sort()

    # funcao para calcular a distancia entre 2 pontos
    def Calcula_distancia(pontoA, pontoB):
        if((pontoA - pontoB) > 0):

            return pontoA - pontoB

        else:

            return pontoB - pontoA

    # algoritmo FCFS
    def FCFS(actual_cilinder, requisitions):

        total_value = 0
        for i in range(len(requisitions)):
            # print('cilindro atual', actual_cilinder,
            #      'proxima requisicao', requisitions[i],)

            total_value += Calcula_distancia(actual_cilinder, requisitions[i])

            actual_cilinder = requisitions[i]

        print('FCFS', total_value)

    # algoritmo SSF
    def SSF(actual_cilinder, requisitions_SSF):

        valor_total = 0
        for i in range(len(requisitions_SSF)-1):

            index = requisitions_SSF.index(actual_cilinder)
            valor_esquerda = Calcula_distancia(
                requisitions_SSF[index], requisitions_SSF[index - 1])
            valor_direita = Calcula_distancia(
                requisitions_SSF[index], requisitions_SSF[index + 1])

            if(valor_esquerda < valor_direita):

                valor_total += valor_esquerda
                actual_cilinder = requisitions_SSF[index - 1]

            else:

                valor_total += valor_direita
                actual_cilinder = requisitions_SSF[index + 1]

            requisitions_SSF.pop(index)

        print('SSF', valor_total)

    # algoritmo SCAN
    def SCAN(last_cilinder, actual_cilinder, requisitions_SCAN):

        valor_total = 0
        direcao_esquerda_direita = True
        for i in range(len(requisitions_SCAN)-2):

            index = requisitions_SCAN.index(actual_cilinder)

            if(requisitions_SCAN[index] == 0):
                direcao_esquerda_direita = False

            if(direcao_esquerda_direita == True):

                valor_total += Calcula_distancia(
                    requisitions_SCAN[index], requisitions_SCAN[index-1])
                actual_cilinder = requisitions_SCAN[index-1]

            else:
                valor_total += Calcula_distancia(
                    requisitions_SCAN[index], requisitions_SCAN[index+1])
                actual_cilinder = requisitions_SCAN[index+1]

            requisitions_SCAN.pop(index)

        print('SCAN', valor_total)

    # chamada das funções
    FCFS(actual_cilinder, requisitions)
    SSF(actual_cilinder, requisitions_SSF)
    SCAN(last_cilinder, actual_cilinder, requisitions_SCAN)
