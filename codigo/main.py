import numpy as np
import sys

# para rodar
# python3 main.py input.txt

# pega o arquivo do terminal
arquivo = sys.argv[1]

# abre e faz matriz
with open(arquivo, 'r') as f:
    input = [[int(num) for num in line.split(' ')] for line in f]


print(input)        # tudo
print(input[0])     # primeira linha
print(input[0][0])  # primeiro elemento, primeira linha

# começa aqui

