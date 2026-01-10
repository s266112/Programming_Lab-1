## PARTE 1: LETTURA DEI DATI DA FILE CSV (10 PUNTI)

# Creare la classe CSVTimeSeriesFile:
# a) La classe deve essere istanziata con il nome del file tramite la variabile name (2 PUNTI)
# b) Deve avere un metodo get_data(country="Italy") che prenda in input il nome di un paese
#    e torni una lista di liste, dove il primo elemento è la data (sotto forma di stringa) ed il 
#    secondo la temperatura media mensile (sotto forma di float) per tutti e SOLO 
#    i valori del paese specificato. (8 PUNTI)


## IDEA: La classe CSVTimeSeriesFile rappresenta un file CSV contenente dati climatici per diversi paesi.
#        Il metodo get_data filtra le righe del file in base al paese richiesto e 
#        restituisce una serie temporale contenente solo dati validi.


# -------------------
# ECCEZIONE PERSONALIZZATA
# -------------------

class ExamException(Exception):
    pass

# --------------------
# CSVTimeSeriesFile
#--------------------

class CSVTimeSeriesFile:

    def __init__ (self, name):

        # Controllo che il nome del file sia una stringa
        if not isinstance (name, str):
            raise ExamException ("Il nome del file deve essere una stringa")
        
        self.name = name

        # Controllo che il file esista ed è apribile
        try:
            open(self.name, 'r').close()                                # Provo ad aprire e chiudere subito il file
        except:
            raise ExamException ("File non trovato o non apribile")     # Se il file non esiste -> Eccezione subito

    def get_data(self, country):

        # Controllo che il nome del paese sia una stringa
        if not isinstance (country, str):
            raise ExamException ("Il nome del paese deve essere una stringa")
        
        dati = []                       # Lista che conterrà i dati del paese richiesto

        file = open(self.name, 'r')     # Provo ad aprire il file
        file.readline()                 # Salto l'intestazione (la prima riga del file)

        # Leggo il file riga per riga
        for riga in file:
            riga = riga.strip()         # Rimuovo spazi bianchi iniziali e finali
            elementi = riga.split(',')  # Divido la riga in base alle virgole

            # Controllo che la riga abbia abbastanza campi
            if len(elementi) < 3:
                continue                # Se non ci sono almeno 4 elementi salto la riga

            data = elementi [0]
            paese = elementi [2].strip().lower()

            # Se il paese non è quello richiesto salto la riga
            if paese != country.strip().lower():
                continue

            # Controllo che la temperatura sia numerica
            try:
                temperatura = float(elementi[1])
            except:
                continue                # Se non è convertibile in float, salto la riga

            # Aggiungo il dato valido alla lista dei dati
            dati.append([data, temperatura])

        # Chiudo il file
        file.close()

        # Se non ho trovato nessun dato valido per il paese
        if len(dati) == 0:
            raise ExamException ("Paese non presente o senza dati validi")
        
        # Ritorno alla lista dei dati
        return dati
    

## PARTE 2: CALCOLO DELLA VARIAZIONE TRA DUE SERIE TEMPORALI (10 PUNTI)

# Creare la funzione  compute_variation, che prende in input due serie temporali, un intervallo di anni
# e restituisce il vettore delle differenze delle medie annuali tra le due time series.
# La funzione deve:
# a) Estrarre le temperature per ciascun anno (2 PUNTI)
# b) Calcolare la media annuale per ogni anno dato (2 PUNTI)
# c) Calcolare la variazione tra le medie anuali delle due serie (4 PUNTI)
# d) Restituire un dizionario con le differenze  (2 PUNTI)

## PARTE 3: ECCEZIONI E CONTROLLO DELL'INPUT (10 PUNTI)
# Le eccezioni devono essere istanziate dalla classe ExamException.
# Devo gestire le seguenti eccezioni:
# a) La classe CSVTimeSeries deve controllare che il file non sia vuoto (2 PUNTI)
# b) La funzione get_data deve controllare che il paese esista nel file (2 PUNTI)
# c) Un valore non numerico oppure non vuoto non deve essere accettato (2 PUNTI)
# d) I valori inseriti devono essere dei numeri interi (2 PUNTI)
# e) L'intervallo selezionato deve essere valido (2 PUNTI)



## IDEA:
# 1. Controllo che gli input siano validi;
# 2. Raggruppo i dati per anno
# 3. Calcolo la media annuale per ogni anno
# 4. Calcolo la differenza tra le due serie
# 5. Ritorno di un dizionario

def compute_variation (time_series_1, time_series_2, first_year, last_year):
    
    # -------------------
    # 1. CONTROLLI INIZIALI
    # -------------------

    # Controllo sugli anni
    if not isinstance (first_year, int) or not isinstance (last_year, int):
        raise ExamException ("Gli anni devono essere interi")
    
    if first_year >= last_year:
        raise ExamException ("Intervallo di anni non valido")
    
    # Controllo sulle serie temporali
    if not isinstance(time_series_1, list) or not isinstance (time_series_2, list):
        raise ExamException ("Le serie temporali devono essere liste")
    
    # ---------------------
    # 2. RAGGRUPPAMENTO PER ANNO
    # ---------------------

    # Dizionari anno -> lista di temperature
    dati_anno_1 = {}
    dati_anno_2 = {}

    # Prima serie temporale
    for elemento in time_series_1:
        data = elemento [0]
        valore = elemento [1]

        anno = int(data.split('-')[0])

        if anno not in dati_anno_1:
            dati_anno_1 [anno] = []

        dati_anno_1[anno].append(valore)

    # Seconda serie temporale
    for elemento in time_series_2:
        data = elemento[0]
        valore = elemento[1]

        anno = int(data.split('-')[0])

        if anno not in dati_anno_2:
            dati_anno_2[anno] = []

        dati_anno_2[anno].append(valore)

    # -----------------
    # 3. CALCOLO MEDIE
    # ----------------- 

    # Dizionari anno -> media annuale
    medie_anno_1 = {}
    medie_anno_2 = {}

    for anno in dati_anno_1:
        valori = dati_anno_1[anno]
        medie_anno_1[anno] = sum(valori) / len(valori)
    
    for anno in dati_anno_2:
        valori = dati_anno_2[anno]
        medie_anno_2[anno] = sum(valori) / len(valori)

    # ------------------
    # 4. CONFRONTO FINALE
    # ------------------

    # Dizionario finale delle variazioni
    variazioni = {}

    for anno in range(first_year, last_year + 1):

        # Controllo che l'anno sia presente in entrambe le serie
        if anno not in medie_anno_1 or anno not in medie_anno_2:
            continue

        # Calcolo la differenza tra le medie annuali
        differenza = medie_anno_1[anno] - medie_anno_2[anno]

        variazioni[anno] = differenza

    return variazioni











