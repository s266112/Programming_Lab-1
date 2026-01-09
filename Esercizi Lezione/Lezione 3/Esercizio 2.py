# Definire una funzione che prende come input un file e conta quante volte ogni parola è presente

# IDEA:
# 1. Apro il file
# 2. Creo un dizionario vuoto
# 3. Leggo il file riga per riga
# 4. Divido ogni riga in parole
# 5. Per ogni parola:
#    a. Se e' nel dizionario incremento il contatore
#    b. Altrimenti la aggiungo al dizionario con contatore a 1
# 6. Ritorno il dizionario


def count_all_words(file_name):
    
    file = open(file_name)      # Apro il file 
    counts = {}                 # Dizionario per i conteggi

    for line in file:           # Leggo il file riga per riga
        words = line.split()    # Divido la riga in parole

    for w in words:             # Per ogni parola nel testo
        w = w.lower()           # La trasformo in minuscolo
        
        if w in counts:
                counts[w] += 1  # Parola gia vista: incremento il contatore
        else:
                counts[w] = 1   # Nuova parola: inizializzo il contatore a 1

    file.close()                # Chiudo il file
    return counts               # Ritorno il dizionario



# Esempio di utilizzo (per test)
print(count_all_words("testo es2.txt"))