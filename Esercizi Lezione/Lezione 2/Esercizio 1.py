## Definire una funzione che prende in input un file ed una parola e conta quante volte quella parola è presente nel file

# IDEA:
# 1. Apro il file
# 2. Leggo il file riga per riga
# 3. Divido ogni riga in parole
# 4. Confronto ogni parola con quella cercata
# 5. Tengo un contatore 
# 6. Ritorno il contatore


def count_word(file_name, word):
    file = open(file_name)      # Apro il file in lettura
    count = 0                   # Contatore delle occorrenze

    for line in file:           # Leggo il file riga per riga
        words = line.split()    # Divido la riga in parole

        for w in words:         # Controllo ogni parola
            if w == word:
                count += 1

    file.close()                # Chiudo il file
    return count                # Ritorno il risultato


# Esempio di utilizzo (per test)
print(count_word("testo es1.txt", "ciao"))

        




