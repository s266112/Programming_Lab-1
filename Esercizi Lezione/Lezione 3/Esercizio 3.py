# Definire una funzione che prende in input un file e costruisce un dizionario con chiavi le lettere iniziali e con valore le parole di lunghezza 
# maggiore contenute nel file che iniziano con quelle lettere.

# IDEA:
# 1. Prendo la prima lettera della parola
# 2. Controllo se la lettera è già nel dizionario:
#   a. Se NON c'e -> inserisco la parola
#   b. Se c'e -> confronto la lunghezza della parola attuale con quella salvata nel dizionario
# 3. Tengo solo la parola più lunga


def parola_iniziale(file_name):

    file = open(file_name)              # Apro il file 
    dizionario = {}                     # Dizionario risultato

    for riga in file:                   # Leggo il file riga per riga
        parole = riga.split()           # Divido la riga in parole

        for parola in parole:           # Per ogni parola nel testo
            parola = parola.lower()     # La trasformo in minuscolo
            iniziale = parola[0]        # Prendo la lettera iniziale

            if iniziale not in dizionario:
                dizionario[iniziale] = parola       # Nuova lettera iniziale: aggiungo la parola
            else:
                # Lettera già presente: confronto le lunghezze
                if len(parola) > len(dizionario[iniziale]):
                    dizionario[iniziale] = parola       # Aggiorno con la parola più lunga

    file.close()                        # Chiudo il file
    return dizionario                   # Ritorno il dizionario

# Esempio di utilizzo (per test)
print(parola_iniziale("testo es3.txt"))