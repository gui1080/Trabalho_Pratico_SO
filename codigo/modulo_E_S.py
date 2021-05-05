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
    # inicializa variaveis ultimo_cilindro e cilindro_atual

    pedidos_SCAN = input.copy()
    ultimo_cilindro = input.pop(0)
    pedidos_SSF = input.copy()
    cilindro_atual = input.pop(0)
    pedidos = input.copy()
    pedidos_SCAN.append(0)

    # ordena a lista de requisitos para os algoritmos SSF e SCAN
    # o objetivo é facilitar o uso da funcao "calcula_distancia" para calcular a distancia entre
    # o cilindro atual e os seus cilindros mais próximos
    pedidos_SSF.sort()
    pedidos_SCAN.sort()

    # funcao para calcular a distancia entre 2 pontos
    def Calcula_distancia(pontoA, pontoB):
        if((pontoA - pontoB) > 0):

            return pontoA - pontoB

        else:

            return pontoB - pontoA

    # algoritmo FCFS (First Come, First Serve)
    # os pedidos são atendidos em ordem de chegada
    def FCFS(cilindro_atual, pedidos):

        resultado_FCFS = 0
        for i in range(len(pedidos)):

            # calcula a distancia entre o pedido do cilindro atual e o que chegou imediatamente depois
            resultado_FCFS += Calcula_distancia(cilindro_atual, pedidos[i])

            cilindro_atual = pedidos[i]

        print('FCFS', resultado_FCFS)

    # algoritmo SSF (Short Seek First)
    # pedidos são atendidos de forma a minimizar o deslocamento do braço de leitura
    def SSF(cilindro_atual, pedidos_SSF):

        resultado_SSF = 0
        for i in range(len(pedidos)):

            # verifica qual e a menor distancia entre o cilindro atual e os cilindros pedidos
            # para decidir se vai seguir pela direita ou esquerda
            # processo se repete até o final da lista de pedidos de acesso
            index = pedidos_SSF.index(cilindro_atual)

            # caso seja o ultimo valor da lista
            if(index + 2 > len(pedidos_SSF)):
                resultado_SSF += Calcula_distancia(
                    pedidos_SSF[index], pedidos_SSF[index - 1])
                cilindro_atual = pedidos_SSF[index - 1]

            else:

                valor_esquerda = Calcula_distancia(
                    pedidos_SSF[index], pedidos_SSF[index - 1])
                valor_direita = Calcula_distancia(
                    pedidos_SSF[index], pedidos_SSF[index + 1])

                if(valor_esquerda < valor_direita):

                    resultado_SSF += valor_esquerda
                    cilindro_atual = pedidos_SSF[index - 1]

                else:

                    resultado_SSF += valor_direita
                    cilindro_atual = pedidos_SSF[index + 1]

            pedidos_SSF.pop(index)

        print('SSF', resultado_SSF)

    # algoritmo SCAN
    # algoritmo atende todos os requisitos em uma direção até chegar a ponta
    # a direção é invertida ao chegar na ponta para atender os pedidos restantes
    def SCAN(ultimo_cilindro, cilindro_atual, pedidos_SCAN):

        resultado_SCAN = 0

        # algoritmo inicialmente começa no sentido esquerda->direita
        direcao_esquerda_direita = True

        for i in range(len(pedidos)+1):

            # caso exista vários pedidos de acesso ao cilindro atual, o index ira apontar para o ultimo
            index = pedidos_SCAN.index(cilindro_atual)

            while(pedidos_SCAN[index] == pedidos_SCAN[index+1]):
                index += 1

            # direção é invertida ao chegar na ponta, se tornando direita->esquerda
            if(pedidos_SCAN[index] == 0):
                direcao_esquerda_direita = False

            if(direcao_esquerda_direita == True):

                resultado_SCAN += Calcula_distancia(
                    pedidos_SCAN[index], pedidos_SCAN[index-1])
                cilindro_atual = pedidos_SCAN[index-1]

            else:
                resultado_SCAN += Calcula_distancia(
                    pedidos_SCAN[index], pedidos_SCAN[index+1])
                cilindro_atual = pedidos_SCAN[index+1]

            pedidos_SCAN.pop(index)

        print('SCAN', resultado_SCAN)

    # chamada das funções

    FCFS(cilindro_atual, pedidos)
    SSF(cilindro_atual, pedidos_SSF)
    SCAN(ultimo_cilindro, cilindro_atual, pedidos_SCAN)

    return 1
