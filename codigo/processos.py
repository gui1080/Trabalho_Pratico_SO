import numpy as np
import sys

def gerencia_de_processos():
    
    # pega o arquivo do terminal
    arquivo = sys.argv[2]

    # abre e faz matriz
    with open(arquivo, 'r') as f:
        input = [[int(num) for num in line.split(' ')] for line in f]

    
    print(input)        # tudo
    print(input[0])     # primeira linha
    print(input[0][0])  # primeiro elemento, primeira linha
    print(len(input))

    qntd = len(input)

    # crio cópias pq os algoritmos ficam eliminando da lista o que não precisa mais fazer
    input_fifo = list(input)
    input_sjf = list(input)
    input_rr = list(input)

    # FIFO  
    # ------------------------------------------------------------------
    
    passagem = 0
    processo_atual = 0
    resposta = 0
    turnaround = 0

    while(True):

        if(input_fifo[0][0] <= passagem):
            # roda na ordem de chegada

            # tempo de resposta é a diferença entre o contador da passagem e o momento que o processo chegou
            # espera é o tempo que o processo aguarda, como ele não para no meio da execução, é igual ao tempo de resposta
            resposta = resposta + (passagem - input_fifo[0][0])
            
            
            duracao = input_fifo[0][1]

            for i in range(duracao):
                print('No momento [', passagem, '] o processo [',  processo_atual,  '] está rodando')
                passagem = passagem + 1

            turnaround = turnaround + (passagem - input_fifo[0][0])

            input_fifo.pop(0)
            processo_atual = processo_atual + 1

            print('\nSobrou então:')
            print(input_fifo)
            print('\n')

        elif(len(input_fifo) != 0):
        
            passagem = passagem + 1

        if(len(input_fifo) == 0):
            print('Fim do FIFO!\n')

            # acumulamos a resposta e o turnaround, dividimos pela quantidade e pegamos a média
            resposta = resposta / qntd
            turnaround = turnaround / qntd

            print('Turnaround: ', turnaround)
            print('Tempo total de execução: ', passagem)
            print('Tempo de espera: ', resposta)
            print('Tempo de resposta: ', resposta)
            print('\n\n')

            break    


    # SJF  
    # ------------------------------------------------------------------

    print(input_sjf)    
    
    passagem = 0
    processo_atual = 0
    resposta = 0
    turnaround = 0

    cpu_ociosa = True
    qntd_restante = qntd

    while(True):

        primeiro = True
        for i in range(qntd_restante):
            if(input_sjf[i][0] <= passagem):
                if(primeiro == True):
                    candidato_atual = i 
                    primeiro = False
                    cpu_ociosa = False

                else:

                    if(input_sjf[i][1] < input_sjf[candidato_atual][1]):
                        candidato_atual = i
            elif(primeiro == True):
                # ainda não achamos nada
                cpu_ociosa = False

        if cpu_ociosa != True:

            duracao = input_sjf[candidato_atual][1]

            resposta = resposta + (passagem - input_sjf[candidato_atual][0])
            
            for i in range(duracao):
                print('No momento [', passagem, '] o processo [',  processo_atual,  '] está rodando')
                passagem = passagem + 1
            
            turnaround = turnaround + (passagem - input_sjf[candidato_atual][0])

            processo_atual = processo_atual + 1
            input_sjf.pop(candidato_atual)
            qntd_restante = qntd_restante - 1
            cpu_ociosa = True
        
        else:

            passagem = passagem + 1

        if(len(input_sjf) == 0):
            print('Fim do SJF!\n')

            # acumulamos a resposta e o turnaround, dividimos pela quantidade e pegamos a média
            resposta = resposta / qntd
            turnaround = turnaround / qntd

            print('Turnaround: ', turnaround)
            print('Tempo total de execução: ', passagem)
            print('Tempo de espera: ', resposta)
            print('Tempo de resposta: ', resposta)
            print('\n\n')

            break    

    # RoundRobin  
    # ------------------------------------------------------------------

    print(input_rr)    
    
    passagem = 0
    processo_atual = 0
    resposta = 0
    turnaround = 0

    duracao = 2

    processos_terminados = []
    contagem_processos_terminados = 0

    while(True):

        # se o processo atual esta na lista de processos terminados, vai pra frente
        if(processo_atual in processos_terminados):
            
            processo_atual = processo_atual + 1
                
            if(processo_atual == qntd):
                processo_atual = 0

        # checamos se a CPU ficou sem nada para fazer naquele instante, por falta de processos
        podemos_executar = False
        for i in range(qntd):
            if(input_rr[i][0] <= passagem):
                podemos_executar = True

        if(podemos_executar == False):
            
            print('A CPU ficou sem nada para fazer na passagem', passagem)
            passagem = passagem + 1

        # se o processo já chegou na nossa passagem, vamos adiante
        if(input_rr[processo_atual][0] <= passagem):

            # confirmando que temos um valor maior que zero a tratar
            if(input_rr[processo_atual][1] > 0):

                # rodamos o processo
                for i in range(duracao):
                    print('No momento [', passagem, '] o processo [',  processo_atual,  '] está rodando')
                    passagem = passagem + 1
                
                # atualizamos o quanto falta daquele processo
                input_rr[processo_atual][1] = (input_rr[processo_atual][1] - duracao) 
                
                # se chegou em zero
                if(input_rr[processo_atual][1] == 0):

                    # adicionamos 1 no contador de processos que terminaram
                    contagem_processos_terminados = contagem_processos_terminados + 1
                    print(contagem_processos_terminados)
                    print(input_rr)

                    # adicionamos na lista de processos terminados aquele em específico
                    processos_terminados.append(processo_atual)
                    print(processos_terminados)

                    turnaround = turnaround + ((passagem+1) - input_rr[processo_atual][0])
                    
                # passamos para o próximo processo
                processo_atual = processo_atual + 1
                
                if(processo_atual == qntd):
                    processo_atual = 0

            # supomos que temos um valor igual a 1 para tratar
            elif(input_rr[processo_atual][1] == 1):
                
                # rodamos o processo
                for i in range(duracao - 1):
                    print('No momento [', passagem, '] o processo [',  processo_atual,  '] está rodando')
                    passagem = passagem + 1
                
                # atualizamos o quanto falta daquele processo
                input_rr[processo_atual][1] = (input_rr[processo_atual][1] - 1) 
                
                # checamos se terminou aquele processo
                if(input_rr[processo_atual][1] == 0):
                    contagem_processos_terminados = contagem_processos_terminados + 1
                    print(contagem_processos_terminados)
                    processos_terminados.append(processo_atual)

                    turnaround = turnaround + ((passagem+1) - input_rr[processo_atual][0])
                
                # passamos pro proximo processo
                processo_atual = processo_atual + 1    
                
                if(processo_atual == qntd):
                    processo_atual = 0
            
        # processo ainda não chegou na nossa cpu, vamos adiante
        else:

            processo_atual + 1

            if(processo_atual == qntd):
                processo_atual = 0

        if(contagem_processos_terminados == qntd):
            print('Fim do RoundRobin!\n')

            # acumulamos a resposta e o turnaround, dividimos pela quantidade e pegamos a média
            #resposta = resposta / qntd
            turnaround = turnaround / qntd

            print('Turnaround: ', turnaround)
            print('Tempo total de execução: ', passagem)
            print('Tempo de espera: ', resposta)
            print('Tempo de resposta: ', resposta)
            print('\n\n')

            break    

    # se chegamos até aqui, deu tudo certo! :)
    return 1

