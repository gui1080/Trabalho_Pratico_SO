# TRABALHO PRÁTICO DE SO - UnB - 2020/02
# Maio de 2021

# Ana Paula - 17/0056082
# Gabriel Matheus - 17/1013498
# Gustavo Carvalho - 17/0058867
# Guilherme Braga - 17/0162290

import sys
from processos import gerencia_de_processos

# pega a operação da linha de comando
op = sys.argv[1]

# para rodar
# python3 main.py x input.txt
# sendo x: 1 para gerência de processos, 2 para gerência de memória e 3 para gerência de E/S


# módulo de gerencia de processos
#---------------------------------------------------

if op == '1':
    processo = gerencia_de_processos()


# módulo de gerencia de memoria
#---------------------------------------------------

#if op == '2':


# módulo de gerencia de E/S
#---------------------------------------------------

#if op == '3':


#---------------------------------------------------

print('Fim da Execução')
