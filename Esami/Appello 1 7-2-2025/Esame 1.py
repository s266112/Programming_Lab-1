## PARTE 1: LEGGERE I DATI E PROCESSARLI (8 PUNTI)

# Creare la classe CSVTimeSeriesFile.
# a) la classe deve essere istanziata con il nome del file tramite la variabile name
# b) Deve avere un metodo get data() che torni una lista di liste, dove il primo elemento delle
#    liste annidate e la data ed il secondo la temperatura media mensile.

# Questa classe si dovra quindi poter usare cosi:
#     time_series_file = CSVTimeSeriesFile(name=’GlobalTemperatures.csv’)
#     time_series = time_series_file.get_data()

## IDEA:
# Un oggetto CSVTimeSeriesFile:
# a. Rappresenta un file CSV temporale
# b. Conosce il nome del file
# c. Sa leggere e filtrare i dati
# d. Restituisce solo dati validi


# ECCEZIONE PERSONALIZZATA
class ExamException(Exception):
    pass

# Costruttore __init_
class CSVTimeSeriesFile:

    def __init__(self, name):
        # Controllo che nome del file sia una stringa
        if not isinstance (name, str):
            raise Exception('Il nome del file deve essere una stringa')
        
        self.name = name

        # Provo ad aprire il file
        try:
            open(self.name, 'r').close()                            # Provo ad aprire e chiudere subito il file
        except:
            raise Exception("File non trovato o non apribile")      # Se il file non esiste -> Eccezione subito

# Metodo get_data
    def get_data (self):
        lista_dati = []                 # Inizializzo la lista dei dati validi

        # Provo ad aprire il file
        file = open(self.name, 'r')
        
        # Leggere e saltare l'intestazione
        file.readline()                 # Salto l'intestazione (la prima riga) del file

        # Leggo il file riga per riga
        for riga in file:
            riga = riga.strip()         # Rimuovo spazi bianchi iniziali e finali
            elementi = riga.split(',')  # Divido la riga in base alle virgole

            # CONTROLLI FONDAMENTALI -> Una riga deve avere almeno 2 elementi (data e temperatura)
            if len (elementi) < 2:
                continue  # Se non ci sono almeno 2 elementi, salto la riga

            # DATA E VALORE
            data = elementi[0]
            

            # Controllo che il valore sia numerico
            try:
                valore = float(elementi[1])
            except:
                continue  # Se non è convertibile in float, salto la riga

            # Aggiungo il dato valido alla lista dei dati
            lista_dati.append([data, valore])

            # Chiudo il file e ritorno la lista dei dati
        file.close()
        return lista_dati
    
## PARTE 2: CALCOLARE LA VARIAZIONE DELLE TEMPERATURE (14 PUNTI)
# Creare una funzione di nome compute_variations che ha come input la serie temporale, l’intervallo ed il parametro N della lunghezza della finestra.
# La funzione dovrà:
# 1. Raggruppare i dati per anno, per gli anni dell’intervallo
# 2. Calcolare la media annuale per ciascun anno
# 3. Calcolare la differenza tra la temperatura media annuale e la media dei 3 anni precedenti
# 4. Restituire un dizionario strutturato cosı: {anno1: variazione1, anno2: variazione2, ...}

##  IDEA: 
# 1. Trasformo time_series in un dizionario di liste per anno
# 2. Calcolo la media annuale per ciascun anno
# 3. Ciclo da first_year a last_year - 1 
# 4. Calcolo le variazioni anno per anno

#------------------------
# SCHELETRO DELLA FUNZIONE
#------------------------

def compute_variations(time_series, first_year, last_year, N):

    #--------------------------
    # CONTROLLI INIZIALI (importantissimi)
    #--------------------------

    if not isinstance (time_series, list):
        raise ExamException ("La serie temporale non è valida")
    
    if not isinstance (first_year, int) or not isinstance (last_year, int):
        raise ExamException ("Gli anni devono essere interi")
    
    if not isinstance (N, int) or N <= 0:
        raise ExamException ("parametro N non valido")
    
    if first_year >= last_year:
        raise ExamException ("Intervallo di anni non valido")
    
    #--------------------------
    # RAGGRUPPO I DATI PER ANNO
    #--------------------------
    dati_per_anno = {}

    # Ora leggo tutta la serie temporale
    for elemento in time_series:
        data = elemento[0]
        valore = elemento[1]

        # Estraggo l'anno in modo robusto (funziona con tutti i formati)
        try:
            anno = int(data[:4])    # Estraggo l'anno dalla data
        except:
            continue                # Se non riesco ad estrarre l'anno, salto questo elemento

        if anno not in dati_per_anno:
            dati_per_anno[anno] = []
        
        dati_per_anno[anno].append(valore)

    #--------------------------
    # CONTROLLO CHE GLI ANNI NECCESSARI ESISTANO NEI DATI
    #--------------------------

    for anno in range(first_year - N, last_year + 1):
        if anno not in dati_per_anno:
            raise ExamException("Anno mancante nella serie temporale")
        
    #--------------------------
    # CALCOLO LA MEDIA ANNUALE PER CIASCUN ANNO
    #--------------------------
    medie_annuali = {}

    for anno in dati_per_anno:
        valori = dati_per_anno[anno]
        medie_annuali[anno] = sum(valori) / len(valori)

    #--------------------------
    # CALCOLO LE VARIAZIONI ANNO PER ANNO
    #--------------------------

    variazioni = {}

    for anno in range (first_year, last_year + 1):
        somma_precedenti = 0

        # Media dei N anni precedenti
        for i in range (1, N + 1):
            somma_precedenti += medie_annuali[anno - i]

        media_precedenti = somma_precedenti / N

        # Variazione rispetto alla media dei N anni precedenti
        variazioni[str(anno)] = medie_annuali[anno] - media_precedenti

        # Ritorno risultato
    return variazioni

# ================================
# TEST DELLA FUNZIONE
# ================================

ts_file = CSVTimeSeriesFile("GlobalTemperatures.csv")
time_series = ts_file.get_data()

print("Prime 5 righe della serie:")
print(time_series[:5])

print("\nVariazioni (1750-1753, N=3):")
print(compute_variations(time_series, 1903, 1906, 3))




