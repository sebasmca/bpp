li = [3, 4, 8, 5, 5, 22, 13]

def es_primo(n):
    return n%2 != 0

primos = list(filter(es_primo,li))
print("Son primos: ", primos)