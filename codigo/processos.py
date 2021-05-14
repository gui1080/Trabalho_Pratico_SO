import sys

# Exemplo de execução:
# python3 main.py 1 input_GerenciadeProcessos.txt

# Por favor não rodar arquivos com espaços desnecessários e quebra de linha ("\n") ao final.

def gerencia_de_processos():

    # pega o arquivo do terminal
    arquivo = sys.argv[2]

    # abre e faz matriz
    with open(arquivo, 'r') as f:
        input = [[int(num) for num in line.split(' ')] for line in f]

    # numero de processos que chegaram
    qntd = len(input)

    # crio cópias pq os algoritmos ficam eliminando da lista o que não precisa mais fazer
    input_fifo = list(input)
    input_sjf = list(input)
    input_rr = list(input)
    
    # especificamente para o roundrobin, vou guardar o tempo que o processo ficou na cpu
    input_original_chegada = []
    input_original_tempo = []

    for i in range(qntd):
        input_original_chegada.append(input[i][1])

    for i in range(qntd):
        input_original_tempo.append(input[i][0])

    # preciamos abrir o arquivo onde o resultado se encontra. Se ele já existe, overwrite. Se não existe, ele é criado.
    f = open("gerencia_de_processos_RESULTADO.txt", "w")

    # FIFO  
    # ------------------------------------------------------------------
    
    f.write("FIFO\n")
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
            
            # tempo que a cpu vai ficar ocupada com aquele processo
            duracao = input_fifo[0][1]

            f.write('Rodar processo [' + str(processo_atual) + '] de [' +  str(passagem) + '] até ['+str(passagem+duracao)+']\n')
            # esse for é a nossa "CPU" rodando o processo
            for i in range(duracao):
                passagem = passagem + 1
            
            # o processo rodou e agora atualizamos o turnaround e a fila do que faltou

            turnaround = turnaround + (passagem - input_fifo[0][0])

            input_fifo.pop(0)
            processo_atual = processo_atual + 1

        # else/if se ninguem rodou e ainda temos processos a rodar, a cpu ficou sem o que fazer esperando o processo
        elif(len(input_fifo) != 0):
            passagem = passagem + 1

        # não tem mais nada na fila para rodar!
        if(len(input_fifo) == 0):

            # acumulamos a resposta e o turnaround, dividimos pela quantidade e pegamos a média
            resposta = resposta / qntd
            turnaround = turnaround / qntd

            # arredondamos a resposta apenas para ter certeza de que vai sair 2 casas decimais no final
            turnaround = round(turnaround, 2)
            resposta = round(resposta, 2)

            print('FIFO: ', turnaround, resposta, resposta)

            break    

    # ao final, escrevemos no arquivo
    resposta = '\n\nFIFO ' + str(turnaround) + ' ' + str(resposta) + ' ' + str(resposta) + '\n\n' 


    # SJF  
    # ------------------------------------------------------------------

    f.write("SJF\n")
    
    passagem = 0
    processo_atual = 0
    resposta = 0
    turnaround = 0

    cpu_ociosa = True
    qntd_restante = qntd

    while(True):

        primeiro = True
        cpu_ociosa = True

        # para todos os processos que faltam
        for i in range(qntd_restante):

            # se o processo já chegou
            if(input_sjf[i][0] <= passagem):

                # se estamos no começo do algoritmo, não tem com o que comparar
                # então o primeiro que satisfez é o menor de qualquer forma
                if(primeiro == True):
                    candidato_atual = i             # atualizamos o processo que vai rodar
                    primeiro = False                # não é mais a primeira vez que o algoritmo roda, na próxima iteração
                    cpu_ociosa = False              # a cpu vai estar ocupada

                # agora, se não é a primeira vez
                else:

                    # e o novo processo testado é menor que o anterior
                    if(input_sjf[i][1] < input_sjf[candidato_atual][1]):
                        candidato_atual = i     # atualizamos o processo que vai rodar
            
            # se terminar sem achar nada, a CPU não vai ter processo para rodar
            elif(primeiro == True):
                # ainda não achamos nada
                cpu_ociosa = True

        # CPU vai rodar o processo certo!
        if cpu_ociosa != True:

            # atualizamos o tempo que o processo vai rodar e o tempo de resposta
            duracao = input_sjf[candidato_atual][1]

            resposta = resposta + (passagem - input_sjf[candidato_atual][0])
            
            f.write('Rodar processo [' + str(processo_atual) + '] de [' +  str(passagem) + '] até ['+str(passagem+duracao)+']\n')
            # esse for é a nossa "CPU" rodando o processo
            for i in range(duracao):
                passagem = passagem + 1
            
            turnaround = turnaround + (passagem - input_sjf[candidato_atual][0])

            # atualizamos as variáveis, vamos testar para os próximos candidatos!
            processo_atual = processo_atual + 1
            input_sjf.pop(candidato_atual)
            qntd_restante = qntd_restante - 1
            cpu_ociosa = True
        
        # não tinha ninguém para rodar, vamos para a próxima passagem
        else:
            
            passagem = passagem + 1

        # acabou a lista de processos a serem executados!
        if(len(input_sjf) == 0):

            # acumulamos a resposta e o turnaround, dividimos pela quantidade e pegamos a média
            resposta = resposta / qntd
            turnaround = turnaround / qntd

            # arredondamos a resposta apenas para ter certeza de que vai sair 2 casas decimais no final
            turnaround = round(turnaround, 2)
            resposta = round(resposta, 2)

            print('SJF: ', turnaround, resposta, resposta)

            break    

    # ao final, escrevemos no arquivo
    resposta = '\n\nSJF ' + str(turnaround) + ' ' + str(resposta) + ' ' + str(resposta) + '\n\n' 

    # RoundRobin  
    # ------------------------------------------------------------------
    f.write("RR\n")

    
    passagem = 0
    processo_atual = 0
    resposta = 0
    turnaround = 0
    espera = 0

    duracao = 2

    processos_terminados = []
    processos_tratados = []
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
            if(input_rr[i][0] <= passagem and i not in processos_terminados):
                podemos_executar = True

        if(podemos_executar == False):
            
            passagem = passagem + 1

        # se o processo já chegou na nossa passagem, vamos adiante
        if(input_rr[processo_atual][0] <= passagem and processo_atual not in processos_terminados):

            # supomos que temos um valor igual a 1 para tratar
            if(input_rr[processo_atual][1] == 1):

                # descobrimos se é a primeira vez dele rodando, para ver o tempo que demorou para dar a resposta
                if(processo_atual not in processos_tratados):
                    resposta = resposta + ((passagem+1) - input_rr[processo_atual][0])
                    processos_tratados.append(processo_atual)
                
                f.write('Rodar processo [' + str(processo_atual) + '] de [' +  str(passagem) + '] até ['+str(passagem+duracao)+']\n')
                # esse for é a nossa "CPU" rodando o processo
                for i in range(duracao):
                    passagem = passagem + 1
                
                # atualizamos o quanto falta daquele processo
                input_rr[processo_atual][1] = (input_rr[processo_atual][1] - 1) 
                
                # checamos se terminou aquele processo
                if(input_rr[processo_atual][1] == 0):
                    contagem_processos_terminados = contagem_processos_terminados + 1
                    processos_terminados.append(processo_atual)

                    turnaround = turnaround + ((passagem+1) - input_rr[processo_atual][0])
                    espera = espera + ((passagem+1) - input_original_chegada[processo_atual] - input_original_tempo[processo_atual])


                # passamos pro proximo processo
                processo_atual = processo_atual + 1    
                
                if(processo_atual == qntd):
                    processo_atual = 0


            # confirmando que temos um valor maior que zero a tratar
            elif(input_rr[processo_atual][1] > 0):

                # descobrimos se é a primeira vez dele rodando, para ver o tempo que demorou para dar a resposta
                if(processo_atual not in processos_tratados):
                    resposta = resposta + ((passagem+1) - input_rr[processo_atual][0])
                    processos_tratados.append(processo_atual)

                f.write('Rodar processo [' + str(processo_atual) + '] de [' +  str(passagem) + '] até ['+str(passagem+duracao)+']\n')
                # esse for é a nossa "CPU" rodando o processo
                for i in range(duracao):
                    passagem = passagem + 1
                
                # atualizamos o quanto falta daquele processo
                input_rr[processo_atual][1] = (input_rr[processo_atual][1] - duracao) 
                

                # se chegou em zero
                if(input_rr[processo_atual][1] == 0):

                    # adicionamos 1 no contador de processos que terminaram
                    contagem_processos_terminados = contagem_processos_terminados + 1

                    # adicionamos na lista de processos terminados aquele em específico
                    processos_terminados.append(processo_atual)

                    turnaround = turnaround + ((passagem+1) - input_rr[processo_atual][0])
                    espera = espera + ((passagem+1) - input_original_chegada[processo_atual] - input_original_tempo[processo_atual])

                # passamos para o próximo processo
                processo_atual = processo_atual + 1
                
                if(processo_atual == qntd):
                    processo_atual = 0
            
        # processo ainda não chegou na nossa cpu, vamos adiante
        
        else:

            temos_o_que_rodar = False

            # se nenhum processo da fila pode rodar, vamos passar adiante sem ninguém rodar
            for i in range(qntd):
                if(input_rr[i][0] <= passagem):
                    # tem algo aqui que podemos rodar!
                    temos_o_que_rodar = True

            if temos_o_que_rodar == False:
                passagem = passagem + 1

            processo_atual = processo_atual + 1

            if(processo_atual == qntd):
                processo_atual = 0

        #print(input_rr)
        #print(qntd)

        if(contagem_processos_terminados == qntd):

            # acumulamos a resposta e o turnaround, dividimos pela quantidade e pegamos a média
            resposta = resposta / qntd
            turnaround = turnaround / qntd
            espera = espera / qntd

            # arredondamos a resposta apenas para ter certeza de que vai sair 2 casas decimais no final
            turnaround = round(turnaround, 2)
            resposta = round(resposta, 2)
            espera = round(espera, 2)

            print('RR: ', turnaround, resposta, espera)

            break    

    # ao final, escrevemos no arquivo
    resposta = '\n\nRR ' + str(turnaround) + ' ' + str(resposta) + ' ' + str(espera) + '\n\n' 

    # fechamos o arquivo
    f.close()

    # se chegamos até aqui, deu tudo certo! :)
    return 1

