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
            
            # tempo que a cpu vai ficar ocupada com aquele processo
            duracao = input_fifo[0][1]

            # esse for é a nossa "CPU" rodando o processo
            for i in range(duracao):
                print('No momento [', passagem, '] o processo [',  processo_atual,  '] está rodando')
                passagem = passagem + 1

            # o processo rodou e agora atualizamos o turnaround e a fila do que faltou

            turnaround = turnaround + (passagem - input_fifo[0][0])

            input_fifo.pop(0)
            processo_atual = processo_atual + 1

            print('\nSobrou então:')
            print(input_fifo)
            print('\n')

        # else/if se ninguem rodou e ainda temos processos a rodar, a cpu ficou sem o que fazer esperando o processo
        elif(len(input_fifo) != 0):
            print('Ninguém chegou ainda na CPU')
            passagem = passagem + 1

        # não tem mais nada na fila para rodar!
        if(len(input_fifo) == 0):
            print('Fim do FIFO!\n')

            # acumulamos a resposta e o turnaround, dividimos pela quantidade e pegamos a média
            resposta = resposta / qntd
            turnaround = turnaround / qntd

            # arredondamos a resposta apenas para ter certeza de que vai sair 2 casas decimais no final
            turnaround = round(turnaround, 2)
            resposta = round(resposta, 2)

            print('Turnaround: ', turnaround)
            print('Tempo total de execução: ', passagem)
            print('Tempo de espera: ', resposta)
            print('Tempo de resposta: ', resposta)
            print('\n\n')

            break    

    # preciamos abrir o arquivo onde o resultado se encontra. Se ele já existe, overwrite. Se não existe, ele é criado.
    f = open("gerencia_de_processos_RESULTADO.txt", "w")

    # ao final, escrevemos no arquivo
    resposta = 'FIFO ' + str(turnaround) + ' ' + str(resposta) + ' ' + str(resposta) + '\n' 
    f.write(resposta)


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
            
            # esse for é a nossa "CPU" rodando o processo
            for i in range(duracao):
                print('No momento [', passagem, '] o processo [',  processo_atual,  '] está rodando')
                passagem = passagem + 1
            
            turnaround = turnaround + (passagem - input_sjf[candidato_atual][0])

            # atualizamos as variáveis, vamos testar para os próximos candidatos!
            processo_atual = processo_atual + 1
            input_sjf.pop(candidato_atual)
            qntd_restante = qntd_restante - 1
            cpu_ociosa = True
        
        # não tinha ninguém para rodar, vamos para a próxima passagem
        else:
            
            print('Ninguém chegou ainda na CPU')
            passagem = passagem + 1

        # acabou a lista de processos a serem executados!
        if(len(input_sjf) == 0):
            print('Fim do SJF!\n')

            # acumulamos a resposta e o turnaround, dividimos pela quantidade e pegamos a média
            resposta = resposta / qntd
            turnaround = turnaround / qntd

            # arredondamos a resposta apenas para ter certeza de que vai sair 2 casas decimais no final
            turnaround = round(turnaround, 2)
            resposta = round(resposta, 2)

            print('Turnaround: ', turnaround)
            print('Tempo total de execução: ', passagem)
            print('Tempo de espera: ', resposta)
            print('Tempo de resposta: ', resposta)
            print('\n\n')

            break    

    # ao final, escrevemos no arquivo
    resposta = 'SJF ' + str(turnaround) + ' ' + str(resposta) + ' ' + str(resposta) + '\n' 
    f.write(resposta)

    # RoundRobin  
    # ------------------------------------------------------------------

    print(input_rr)    
    
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
            
            print('A CPU ficou sem nada para fazer na passagem ', passagem)
            passagem = passagem + 1

        # se o processo já chegou na nossa passagem, vamos adiante
        if(input_rr[processo_atual][0] <= passagem and processo_atual not in processos_terminados):

            # supomos que temos um valor igual a 1 para tratar
            if(input_rr[processo_atual][1] == 1):

                # descobrimos se é a primeira vez dele rodando, para ver o tempo que demorou para dar a resposta
                if(processo_atual not in processos_tratados):
                    print('Primeira vez por aqui, não é mesmo?')
                    resposta = resposta + ((passagem+1) - input_rr[processo_atual][0])
                    processos_tratados.append(processo_atual)
                
                # esse for é a nossa "CPU" rodando o processo
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
                    espera = espera + ((passagem+1) - input_original_chegada[processo_atual] - input_original_tempo[processo_atual])


                # passamos pro proximo processo
                processo_atual = processo_atual + 1    
                
                if(processo_atual == qntd):
                    processo_atual = 0


            # confirmando que temos um valor maior que zero a tratar
            elif(input_rr[processo_atual][1] > 0):

                # descobrimos se é a primeira vez dele rodando, para ver o tempo que demorou para dar a resposta
                if(processo_atual not in processos_tratados):
                    print('Primeira vez por aqui, não é mesmo?')
                    resposta = resposta + ((passagem+1) - input_rr[processo_atual][0])
                    processos_tratados.append(processo_atual)

                # esse for é a nossa "CPU" rodando o processo
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
            print('Fim do RoundRobin!\n')

            # acumulamos a resposta e o turnaround, dividimos pela quantidade e pegamos a média
            resposta = resposta / qntd
            turnaround = turnaround / qntd
            espera = espera / qntd

            # arredondamos a resposta apenas para ter certeza de que vai sair 2 casas decimais no final
            turnaround = round(turnaround, 2)
            resposta = round(resposta, 2)
            espera = round(espera, 2)

            print('Turnaround: ', turnaround)
            print('Tempo total de execução: ', passagem)
            print('Tempo de espera: ', espera)
            print('Tempo de resposta: ', resposta)
            print('\n\n')

            break    

    # ao final, escrevemos no arquivo
    resposta = 'RR ' + str(turnaround) + ' ' + str(resposta) + ' ' + str(espera) + '\n' 
    f.write(resposta)

    # fechamos o arquivo
    f.close()

    # se chegamos até aqui, deu tudo certo! :)
    return 1

