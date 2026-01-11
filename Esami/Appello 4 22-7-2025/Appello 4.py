## PARTE 1: LETTURA E FILTRAGGIO DATI (10 PUNTI)

# Scrivere la classe CSVTimeSeriesFile:
# a. La classe deve essere istanziata con il nome del file tramite la variabile name (2 PUNTI).
# b. Deve avere un metodo get data che torni una lista di liste, dove il primo elemento 
#    è la data (stringa) e il secondo la temperatura media mensile (float).
#    La temperatura deve essere salvata solo se la variazione associata a quel valore
#    è minore di 5 gradi (8 PUNTI)

# -------------------
# ECCEZIONE PERSONALIZZATA
#--------------------

class ExamException(Exception):
    pass

# -----------
# LETTURA FILE CSV
#--------------

class CSVTimeSeriesFile:

    def __init__(self, name):

        # Controllo che il nome del file sia una stringa
        if not isinstance (name, str):
            raise ExamException ("Il nome del file deve essere una stringa")
        
        self.name = name

        # Controllo che il file esista e sia apribile
        try:
            open (self.name, 'r').close()
        except:
            raise ExamException ("File non trovato o non apribile")
        
    def get_data (self):

        # Lista che conterrà i dati validi (data, temperatura)
        dati = []                           
        
        # Variabile che tiene la temperatura del mese precedente
        precedente = None                  

        # Apro il file e leggo l'intestazione
        file = open(self.name, 'r')         # Provo ad aprire il file
        file.readline()                     # Salto l'intestazione (la prima riga del file)
        
        # Leggo il file riga per riga
        for riga in file:
            riga = riga.strip()            # Rimuovo spazi bianchi iniziali e finali
            elementi = riga.split(',')     # Divido la riga in colonne

            # Controllo che ci siano almeno Data e Temperatura
            if len(elementi) < 2:
                continue                   # Se non ci sono almeno 2 elementi salto la riga

            # Estraggo la data (stringa)
            data = elementi [0]

            # Provo a convertire la temperatura in float
            try:
                temperatura = float(elementi[1])
            except:
                continue                # Se non è convertibile in float, salto la riga

            # Se ho gia una temperatura precedente, confronto la variazione
            if precedente is not None:
                variazione = abs (temperatura - precedente)

                # Se la variazione è >=5, scarto il mese
                if variazione >= 5:
                    print (f"Mese {data} scartato per variazione >= 5")
                    precedente = temperatura
                    continue

            # Se il mese è valido, lo aggiungo ai dati
            dati.append([data, temperatura])

            # Aggirno la temperatura precedente
            precedente = temperatura

        # Chiudo il file
        file.close()

        # Se non ho trovato nessun dato valido, lancio l'eccezione
        if len(dati) == 0:
            raise ExamException("Nessun dato valido disponibile")
        
        # Ritorno la serie temmporale pulita
        return dati


## PARTE 2: ANALISI DELLA VARIABILE ANNUALE (10 PUNTI)

# Definire la funzione compute_month_variation (time_series, first_year, second_year) che calcoli la variazione nel valore della temperatura tra lo
# stesso mese, tra il second_year ed il first_year.

# a. Raggruppare le temperature per anno, per i due anni considerati (3 PUNTI)
# b. Considerare solo i mesi presenti in entrambi gli anni. (2 PUNTI)
# c. Fare le differenze mensili tra i mesi (2 PUNTI).
# d. Ritornare un dizionario con chiave i mesi e valore la variazione per quel mese (2 PUNTI)

## PARTE 3: VALUTAZIONE INPUT ED ECCEZZIONI

# Le eccezzioni devo gestire i seguenti casi:
# a. La classe CSVTimeSeriesFile deve controllare l’esistenza del file in get_data e, nel caso il file non esista, alzare un’eccezione (2 PUNTI).
# b. Stampare un messaggio quando viene saltato perchè l'incertezza e > =5 (2 PUNTI)
# c. I due anni devono essere numeri interi col primo strettamente minore del secondo (2 PUNTI).
# d. Se un mese non è presente in uno o entrambi gli anni (2 PUNTI).
# e. Se nessun mese è disponibile, alzare un eccezione (2 PUNTI).

def compute_month_variation (time_series, first_year, second_year):
    
    # --------------
    # CONTROLLI INIZIALI
    # ---------------

    # Controllo che gli anni siano interi
    if not isinstance (first_year, int) or not isinstance (second_year, int):
        raise ExamException ("Errore: Gli anni devono essere interi")
    
    # Controllo che gli anni siano diversi 
    if first_year == second_year:
        raise ExamException ("Errore: I due anni devono essere diversi")
    
    # Controllo che la serie temporale sia una lista
    if not isinstance(time_series, list):
        raise ExamException ("Errore: La serie temporale deve essere una lista")
    
    #------------------
    # INIZIALIZZAZIONE STRUTTURE DATI
    # -----------------

    # Dizionario mesi 
    dati_primo_anno = {}            # Temperatura per il primo anno
    dati_secondo_anno = {}          # Temperatura per il secondo anno

    # --------------------
    # SEPARAZIONE DEI DATI PER ANNO E MESE
    # --------------------

    # Scorro tutta la serie temporale
    for elemento in time_series:
        data = elemento [0]
        temperatura = elemento [1]

        # Divido la data per estrarre anno e mese
        parti = data.split('/')
        giorno = parti[0]
        mese = parti [1]
        anno = int(parti[2])
        
        # Se la data appartiene al primo anno, lo salvo
        if anno == first_year:
            dati_primo_anno[mese] = temperatura

        # Se il dato appartiene al secondo anno, lo salvo
        elif anno == second_year:
            dati_secondo_anno[mese] = temperatura


    # -----------------
    # CONFRONTO DEI MESI IN COMUNE
    # -----------------

    # Dizionario che conterrà le differenze valide mese -> variazione
    differenze = {}

    # Confronto solo i mesi presenti in entrambi gli anni
    for mese in dati_primo_anno:

        # Se il mese non è presente anche nel secondo anno, lo scarto
        if mese not in dati_secondo_anno:
            print(f"Mese {mese} non presente in entrambi gli anni")
            continue

        # Calcolo la differenza di temperatura tra i due anni
        diff = dati_secondo_anno[mese] - dati_primo_anno[mese]
        
        # Se la variazione è troppo grande, scarto il mese
        if abs(diff) >= 5:
            print(f"Mese {mese} scartato per variazione >= 5")
            continue

        # Se il mese è valido, salvo la differenza
        differenze[mese] = diff

    # --------------
    # CONTROLLO FINALE
    # --------------

    # Se non ho trovato nessuna differenza valida, lancio eccezione
    if len(differenze) == 0:
        raise ExamException ("Errore: nessuna differenza mensile trovata")
    
    # Ritorno il dizionario delle differenze
    return differenze



    
            