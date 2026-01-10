## PARTE 1: LETTURA E FILTRAGGIO DATI (10 PUNTI)
# Scrivere la classe CSVTimeSeriesFile:
# a. La classe deve essere istanziata con il nome del file tramite la variabile name (2 PUNTI).
# b. Deve avere un metodo get data che prende in input il nome della città, e restituisce una lista di coppie [data,temperatura], 
#    dove il primo elemento è la data (sotto forma di stringa) e il secondo la temperatura media mensile (sotto forma di float), 
#    per tutti e SOLO i valori della città in input validi, quindi scritti come valori di tipo float (8 PUNTI).

## IDEA: La classe CSVTimeSeriesFile rappresenta un file CSV contenente 
#        dati climatici per diverse città. Il metodo get_data filtra i dati in base alla 
#        citta richiesta e restituisce una serie temporale contenente solo dati validi.

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

    def get_data(self, city):

        # Controllo che il nome dela città sia una stringa
        if not isinstance (city, str):
            raise ExamException ("Il nome della città deve essere una stringa")
        
        dati = []                       # Lista che conterrà i dati della città richiesta

        file = open(self.name, 'r', encoding='utf-8')     # Provo ad aprire il file
        file.readline()                                   # Salto l'intestazione (la prima riga del file)

        # Leggo il file riga per riga
        for riga in file:
            riga = riga.strip()         # Rimuovo spazi bianchi iniziali e finali
            elementi = riga.split(',')  # Divido la riga in base alle virgole

            # Controllo numero colonne
            if len(elementi) < 4:
                continue                # Se non ci sono almeno 4 elementi salto la riga

            data = elementi [0]
            citta = elementi [3].strip().lower()

            # Se la città non è quello richiesto salto la riga
            if citta != city.strip().lower():
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

        # Se non ho trovato nessun dato valido per la città
        if len(dati) == 0:
            raise ExamException ("Città non presente o senza dati validi")
        
        # Ritorno alla lista dei dati
        return dati
    

## PARTE 2: CALCOLO DEL COEFFICENTE ANGOLARE (10 PUNTI)
# Definire la funzione compute_slope(time series, first year, last year) che prende in input una serie temporale, anno iniziale e finale 
# dell’intervallo di anni da considerare (inclusi) e ritorna il coefficiente angolare della retta di regressione sugli anni considerati. 
# Gli anni dell’intervallo sono inseriti come tipi interi. La funzione deve in particolare:
# a. Raggruppare le temperature per anno nel range specificato (inclusivo), considerando solo gli anni 
#    per cui sono disponibili almeno 6 misurazioni mensili valide. (2 PUNTI)
# b. Calcolare la media annuale per ogni anno valido nell’intervallo dato (2 PUNTI).
# c. Calcolare la media di tutti gli anni ¯x, e il valore medio delle temperature medie annuali ¯y (2 PUNTI)
# d. Calcolare e poi ritornare il coefficiente angolare m (4 PUNTI).

## PARTE 3: VALUTAZIONE INPUT ED ECCEZZIONI
# Le eccezzioni devo gestire i seguenti casi:
# a. La classe CSVTimeSeriesFile deve controllare l’esistenza del file in get_data e, nel caso il file non esista, alzare un’eccezione (2 PUNTI).
# b. Se il nome della città dato in input non `e presente nel file, si deve alzare una eccezione (2 PUNTI)
# c. Se n risulta uguale a zero o il denominatore nel calcolo del coefficiente angolare risulta uguale a zero sollevare un’eccezione (2 PUNTI).
# d. Se l’intervallo di anni fornito `e vuoto o non valido, sollevare un’eccezione (2 PUNTI).
# e. Se un anno contiene meno di 6 valori validi, bisogna ignorarlo (non si tratta di un errore, ma di un caso da gestire) (2 PUNTI).

## IDEA:
# 1. Controllo che gli input siano validi;
# 2. Raggruppo i dati per anno
# 3. Filtro almeno 6 mesi per anno
# 4. Calcolo le medie annuali
# 5. Controllo almeno 2 anni validi
# 6. Applico formula della regressione lineare (slope) per ottenere il coefficente angolare

def compute_slope (time_series, first_year, last_year):
    
    # -------------------
    # 1. CONTROLLI INIZIALI
    # -------------------

    # Controllo che gli anni siano interi
    if not isinstance (first_year, int) or not isinstance (last_year, int):
        raise ExamException ("Gli anni devono essere interi")
    
    # Controllo che l'intervallo sia valido
    if first_year >= last_year:
        raise ExamException ("Intervallo di anni non valido")
    
    # Controllo che la serie temporale sia una lista
    if not isinstance(time_series, list):
        raise ExamException ("La serie temporale deve essere una lista")
    
    # ---------------------
    # 2. RAGGRUPPAMENTO PER ANNO
    # ---------------------

    dati_per_anno = {}
 
    for elemento in time_series:
        data = elemento [0]
        valore = elemento [1]

        # Estraggo l'anno dalla data (YYYY-MM-DD)
        anno = int(data.split('-')[0])

        # Considero solo gli anni nell'intervallo
        if anno < first_year or anno > last_year:
            continue

        if anno not in dati_per_anno:
            dati_per_anno[anno] = []
        
        dati_per_anno[anno].append(valore)

    # -----------------
    # 3. FILTRO: ALMENO 6 MESI L'ANNO
    # ----------------- 

    anni_validi = {}

    for anno in dati_per_anno:
        if len (dati_per_anno[anno]) >=6:
            anni_validi[anno] = dati_per_anno[anno]

    # Servono almeno due anni per calcolare la slope
    if len(anni_validi) < 2:
        raise ExamException ("Dati insufficenti per calcolare la slope")
    

    # ------------------
    # 4. CALCOLO MEDIE ANNUALI
    # ------------------

    medie_annuali = {}

    for anno in anni_validi:
        valori = anni_validi[anno]
        medie_annuali[anno] = sum(valori) / len(valori)

    # --------------------
    # CALCOLO SLOPE (REGRESSIONE LINEARE)
    # --------------------

    # Lista degli anni (x) e delle medie (y)
    anni = list(medie_annuali.keys())
    temperature = list(medie_annuali.values())

    # Media di x e y
    x_media = sum(anni) / len(anni)
    y_media = sum(temperature) / len(temperature)

    # Numeratore e denominatore della formula
    numeratore = 0
    denominatore = 0

    for i in range(len(anni)):
        numeratore += (anni[i] - x_media) * (temperature[i] - y_media)
        denominatore += (anni[i] - x_media) ** 2

    # Se il denominatore è zero non posso dividere
    if denominatore == 0:
        raise ExamException("Impossibile calcolare la slope")

    slope = numeratore / denominatore

    return slope


