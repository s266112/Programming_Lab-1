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

        # 1. Controllo che il nome del file sia una stringa
        if not isinstance (name, str):
            raise ExamException ("Il nome del file deve essere una stringa")
        
        self.name = name

        # 2. Controllo che il file esista ed è apribile in lettura. Se fallisce alzo un'eccezione
        try:
            file = open(self.name, 'r')                                     # Provo ad aprire il file
            file.close()                                                    # Chiudo il file
        except:
            raise ExamException ("Errore: Impossibile aprire il file")      # Se il file non esiste -> Eccezione 

    def get_data(self, city):

        # 1. Controllo input funzione
        if not isinstance (city, str):
            raise ExamException ("Il nome della città deve essere una stringa")
        
        # Inizializzo la lista dei risultati
        dati_citta = []

        # Flag per sapere se ho trovato almeno una volta la citta
        citta_trovata = False

        try:
            file = open(self.name, 'r')     # Provo ad aprire il file
            file.readline()                 # Salto l'intestazione (la prima riga del file)
        except:
            raise ExamException ("Errore: Impossibile aprire il file")

        # 2. Leggo il file riga per riga
        for riga in file:
            riga = riga.strip()         # Rimuovo spazi bianchi iniziali e finali
            elementi = riga.split(',')  # Divido le colonne

            # Controllo CSV: mi aspetto almeno 4 colonne
            if len(elementi) < 4:
                continue                # Se non ci sono almeno 4 elementi salto la riga

            # 3. Estrazione dati
            data = elementi [0]

            # Pulizia nome città (tolgo gli spazi e metto minuscolo per confronto sicuro)
            citta_csv = elementi[3].strip().lower()
            city_input = city.strip().lower()

            # 4. Filtro per Citta
            if citta_csv!= city_input:
                continue                # Se non è la città che cerco passo alla prosima riga

            # Se arrivo qui, la citta è quella giusta
            citta_trovata = True

            # 5. Controllo Validità Temperatura
            try:
                temperatura = float(elementi[1])
            except:
                continue                # Se c'e un valore nullo o testo, salto la riga

            # Salvo la coppia [data, temperatura]
            dati_citta.append([data, temperatura])

        # Chiudo il file
        file.close()

        # 6. Controllo finale: Se la città non è mai comparsa o non ha dati validi -> Errore
        if not citta_trovata or len(dati_citta) == 0:
            raise ExamException ("Errore: La citta non è presente nel file o non ha dati")
        
        # Ritorno alla lista dei dati
        return dati_citta
    

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


# ---------------------
# FUNZIONE compute_slope (Calcolo Coefficente Angolare)
# ---------------------

def compute_slope (time_series, first_year, last_year):
    
    
    # --- 1. CONTROLLI INIZIALI ---
    
    # Controllo che gli anni siano interi
    if not isinstance (first_year, int) or not isinstance (last_year, int):
        raise ExamException ("Errore: Gli anni devono essere interi")
    
    # Controllo che l'intervallo sia valido
    if first_year >= last_year:
        raise ExamException ("Errore: Intervallo di anni non valido")
    
    # Controllo che la serie temporale sia una lista
    if not isinstance(time_series, list):
        raise ExamException ("Erroe: time_series deve essere una lista")
    
    # --- 2. RAGGRUPPAMENTO DATI PER ANNO ---
    
    dati_per_anno = {}
 
    for row in time_series:
        data_str = row [0]
        temp = row [1]

        # Estraggo l'anno dalla data (YYYY-MM-DD)
        try:
            anno = int(data_str.split('-')[0])
        except:
            continue            # Salto date malformate

        # Considero solo gli anni nell'intervallo richiesto [first, last] inclusi
        if anno < first_year or anno > last_year:
            continue

        if anno not in dati_per_anno:
            dati_per_anno[anno] = []
        
        dati_per_anno[anno].append(temp)

    
    # --- 3. FILTRO "ALMENO 6 MESI" E CALCOLO MEDIE

    medie_annuali = {}      # Questo sarà il mio asse Y (Temperature)
    anni_validi = []        # Questo sarà il mio asse X (Anni)
   
    for anno, lista_temperature in dati_per_anno.items():
        if len (lista_temperature) >=6:
            media = sum(lista_temperature) / len (lista_temperature)

            medie_annuali[anno] = media
            anni_validi.append(anno)

    # Ordino gli anni per sicurezza (fondamentale per la regressione temporale)
    anni_validi.sort()

    # --- 4. CONTROLLI MATEMATICI PRE-CALCOLO ---

    # Servono almeno 2 punti per fare una retta (quindi una slope)
    if len(anni_validi) < 2:
        raise ExamException ("Errore: Dati insufficenti (meno di 2 anni validi) per calcolare la slope")
    
    #  --- 5. CALCOLO DELLA SLOPE 
    # Formula: m = sum((x - media_x) * (y - media_y)) / sum((x - media_x)^2)

    # A. Preparo le liste X e Y allineate
    valori_x = anni_validi                                  # Anni
    valori_y = [medie_annuali[a] for a in anni_validi]      # Temperature medie corrispondenti

    # B. Calcolo le medie totali (x_bar e y_bar)
    media_x = sum(valori_x) / len(valori_x)
    media_y = sum(valori_y) / len(valori_y)

    numeratore = 0
    denominatore = 0

    # C. sommatorie
    for i in range(len(valori_x)):
        x_diff = valori_x[i] - media_x
        y_diff = valori_y[i] - media_y

        numeratore += x_diff * y_diff
        denominatore += x_diff ** 2

    # D. Controllo divisione per zero

    if denominatore == 0:
        raise ExamException("Errore: Impossibile calcolare la slope (denominatore nullo)")

    slope = numeratore / denominatore

    return slope

# ===============================
# CODICE DI TEST AUTOMATICO
# ===============================
if __name__ == "__main__":
    print("--- INIZIO TEST ---\n")

    # 1. Creazione file CSV finto
    filename = "test_slope.csv"
    csv_data = """dt,AverageTemperature,AverageTemperatureUncertainty,City,Country,Latitude,Longitude
1900-01-01,10.0,0.5,Rome,Italy,41N,12E
1900-02-01,10.0,0.5,Rome,Italy,41N,12E
1900-03-01,10.0,0.5,Rome,Italy,41N,12E
1900-04-01,10.0,0.5,Rome,Italy,41N,12E
1900-05-01,10.0,0.5,Rome,Italy,41N,12E
1900-06-01,10.0,0.5,Rome,Italy,41N,12E
1901-01-01,20.0,0.5,Rome,Italy,41N,12E
1901-02-01,20.0,0.5,Rome,Italy,41N,12E
1901-03-01,20.0,0.5,Rome,Italy,41N,12E
1901-04-01,20.0,0.5,Rome,Italy,41N,12E
1901-05-01,20.0,0.5,Rome,Italy,41N,12E
1901-06-01,20.0,0.5,Rome,Italy,41N,12E
"""
    # Spiegazione Test Matematico:
    # Anno 1900: Ho 6 mesi tutti a 10.0 -> Media 1900 = 10.0
    # Anno 1901: Ho 6 mesi tutti a 20.0 -> Media 1901 = 20.0
    # Retta che passa per (1900, 10) e (1901, 20).
    # Slope (pendenza) = (y2 - y1) / (x2 - x1) = (20 - 10) / (1901 - 1900) = 10 / 1 = 10.0

    try:
        with open(filename, "w") as f:
            f.write(csv_data)
        
        # Test 1: Lettura
        print("1️⃣  Lettura file...")
        ts_file = CSVTimeSeriesFile(filename)
        data = ts_file.get_data("Rome")
        print(f"   Dati letti: {len(data)} righe (attese 12).")

        # Test 2: Slope
        print("\n2️⃣  Calcolo Slope (atteso 10.0)...")
        slope = compute_slope(data, 1900, 1901)
        print(f"   Slope calcolata: {slope}")
        
        if abs(slope - 10.0) < 0.001:
            print("   ✅ Test Superato!")
        else:
            print("   ❌ Errore nel calcolo.")

    except ExamException as e:
        print(f"❌ Errore catturato: {e}")
    except Exception as e:
        print(f"❌ Errore generico: {e}")

    print("\n--- FINE TEST ---")


