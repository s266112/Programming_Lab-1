# Definire una funzione che prende come input un file, rimuove tutte le righe duplicate, scrive il risultato in un nuovo file chiamato unique.txt.

# IDEA:
# 1. Apro il file di input
# 2. Leggo il file riga per riga
# 3. Tengo traccia delle righe già viste in una lista
# 4. Per ogni riga:
#    a. Se la riga non è ancora stata vista -> la salvo
# 5. Scrivo le righe uniche in un nuovo file chiamato unique.txt


def legge_file(file_name):  # Definisco una funzione

    # Apro il file di input
    file = open(file_name, 'r')

    # Inizializzo struttura dati per contenere il testo
    righe_viste = set()     # Insieme delle righe gia incontrate
    righe_uniche = []       # Lista delle senza duplicati

    # Leggo il file riga per riga
    for riga in file:
        # Controllo se la riga è già stata vista
        if riga not in righe_viste:
            righe_viste.add(riga)        # Aggiungo la riga all'insieme delle viste
            righe_uniche.append(riga)    # Aggiungo la riga alla lista delle uniche
            
    # Chiudo il file di input
    file.close()

    # Scrivo il file unique.txt con le righe uniche
    file_out = open('unique.txt', 'w')  # Apro il file di output in scrittura
    
    # Scrivo le righe uniche nel file di output
    for riga in righe_uniche:
        file_out.write(riga)    # Scrivo la riga nel file di output
    
    file_out.close()            # Chiudo il file di output

# Esempio di utilizzo (per test)
legge_file("testo es5.txt")
    
    