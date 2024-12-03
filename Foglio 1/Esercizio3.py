# Scrivere una funzione che prende in input una stringa e ritorna True se è un palindromo, False altrimenti.

def palindromo(stringa):
    n = len(stringa)
    for i in range(n // 2):                     # Confronta fino alla metà della stringa
        if stringa[i] != stringa[n - i - 1]:    # Confronta i caratteri opposti
            return -1                           # Non è un palindromo
    return 1                                    # È un palindromo

# Esempio di utilizzo
print(palindromo("anna"))  # 1
print(palindromo("pollo"))  # -1