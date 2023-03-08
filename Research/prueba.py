import itertools

numeros = ["3", "5", "6", "4"]
combinaciones = itertools.permutations(numeros, 4)

for combinacion in combinaciones:
    print(combinacion)
