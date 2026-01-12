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
            open(self.name, 'r').close()                                         # Provo ad aprire e chiudere subito il file
        except:
            raise ExamException ("Errore: File non trovato o non apribile")      # Se il file non esiste -> Eccezione subito

# Metodo get_data
    def get_data (self):
        lista_dati = []                 # Inizializzo la lista dei dati validi

        # Provo ad aprire il file
        try: 
            file = open(self.name, 'r')
            file.readline()                 # Salto l'intestazione (la prima riga) del file
        except:
            raise ExamException ("Errore in lettura file")


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
                continue        # Se non è convertibile in float, salto la riga

            if valore < 0:
                continue        # Se il valore è negativo non deve essere accettato

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
    
    if N>= (last_year - first_year + 1):
        raise ExamException ("Il parametro deve essere minore dell'intervallo considerato")
    
    #--------------------------
    # RAGGRUPPO I DATI PER ANNO
    #--------------------------
    dati_per_anno = {}

    # Ora leggo tutta la serie temporale
    for elemento in time_series:
        data = elemento[0]
        valore = elemento[1]

        # Estraggo l'anno
        try:
            # Assumo che i primi 4 caratteri siano l'anno (es. 1900/01)
            anno = int(data[:4]) 
        except:
            continue                # Se non riesco ad estrarre l'anno, salto questo elemento

        if anno not in dati_per_anno:
            dati_per_anno[anno] = []
        
        dati_per_anno[anno].append(valore)


    #--------------------------
    # CALCOLO LA MEDIA ANNUALE PER CIASCUN ANNO
    #--------------------------
    medie_annuali = {}

    # Calcolo la media solo se ho i dati per quell'anno
    for anno in dati_per_anno:
        valori = dati_per_anno[anno]
        if len(valori) > 0:
            medie_annuali[anno] = sum(valori) / len(valori)

    #--------------------------
    # CALCOLO LE VARIAZIONI ANNO PER ANNO
    #--------------------------

    variazioni = {}

    # Ciclo sugli anni richiesti dall'intervallo
    for anno_target in range (first_year, last_year + 1):

        # Se l'anno target non ha dati, non posso calcolare nulla
        if anno_target not in medie_annuali:
            continue

        # Controllo se esistano gli N anni precedenti
        # Gli anni precedenti sono: anno-1, anno-2... fino a anno-N
        anni_precedenti_ok = True
        somma_precedenti = 0
        
        # Media dei N anni precedenti
        for i in range (1, N + 1):
            anno_prev = anno_target - i
            if anno_prev in medie_annuali:
                somma_precedenti += medie_annuali[anno_prev]
            else:
                anni_precedenti_ok = False
                break                       # Manca un anno precedente, interrompo

        # Se ho tutti gli anni precedenti necessari, calcolo la variazione
        if anni_precedenti_ok:
            media_mobile = somma_precedenti / N
            diff = medie_annuali[anno_target] - media_mobile

            # Salvo nel dizionario (chiave stringa come esempio esame)
            variazioni[str(anno_target)] = diff
            
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




