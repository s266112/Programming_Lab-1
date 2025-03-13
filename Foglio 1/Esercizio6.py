# Definite la funzione fattoriale

def fattoriale(n):
    risultato = 1
    for i in range(1, n + 1):
        risultato *= i
    return risultato

n = 3
print (fattoriale(n))  