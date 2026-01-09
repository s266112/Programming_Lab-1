# Definire una funzione conteggio che prende come input un file e ritorna un dizionario con chiave la prima parola di ogni frase e 
# valore il numero di volte che una frase inizia con quella parola. Considerare come inizio di frase qualsiasi parola che segue un punto, 
# un punto esclamativo, un punto interrogativo o si trova all'inizio del testo.

# IDEA:
# 1. Apro il file e leggo il contenuto
# 2. Lo divido in frasi usando come separatori ., !, ?
# 3. Per ogni frase:
#    a. Tolgo gli spazi iniziali e finali
#    b. Se la frase non è vuota prendo la prima parola
#    c. La trasformo in minuscolo
#  4. Aggiorno il dizionario con la parola iniziale:
#    a. Se non è presente la aggiungo con contatore a 1
#    b. Se è presente incremento il contatore di 1


def conteggio(file_name):      # Definisco una funzione

    # Inizializzo un dizionario vuoto
    dizionario = {}

    # Apro e leggo tutto il file e lo chiudo
    file = open(file_name, 'r')     # Apro il file
    testo = file.read()             # Leggo il contenuto
    file.close()                    # Chiudo il file

    # Rendo uniformi i separatori di frase
    testo = testo.replace ('!','.')
    testo = testo.replace ('?','.')    # Ora tutte le frasi finiscono con un '.' (punto)

    # Divido il testo in frasi usando il punto come separatore
    frasi = testo.split('.')

    # Analizzo una frase alla volta
    for frase in frasi:
        frase = frase.strip()         # Tolgo gli spazi iniziali e finali
    
    # Controllo che la frase non sia vuota
        if frase == "":
            continue                  # Frase vuota: passo alla successiva

    # Prendo la prima parola della frase e la metto in minuscolo
        parole = frase.split()              # Divido la frase in parole
        prima_parola = parole[0].lower()    # Prima parola in minuscolo

    # Aggiorno il dizionario
        if prima_parola in dizionario:
            dizionario [prima_parola] += 1     # Parola già presente: incremento il contatore
        else:
            dizionario [prima_parola] = 1      # Nuova parola: inizializzo il contatore a 1

    # Ritorno il dizionario risultato
    return dizionario

# Esempio di utilizzo (per test)
print(conteggio("testo es4.txt"))