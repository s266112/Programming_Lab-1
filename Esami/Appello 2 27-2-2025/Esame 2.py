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
            file = open(self.name, 'r')           # Provo ad aprire il file in lettura
            linea = file.readline()               # Provo a leggere una riga
            file.close ()                         # Chiudo il file

            # Controllo se il file è vuoto come richiesto (Avviene dentro il TRY) -> Serve quando funziona tutto ma file vuoto
            if not linea:
                raise ExamException ("Errore: Il file è vuoto o non contiene dati validi")
            
        # Controllo se il file è apribile
        except FileNotFoundError:
            raise ExamException ("Errore: Impossibile aprire il file")
        
        # Controllo se il file è vuoto o illegibile (avviene dentro EXCEPT) -> Serve quando qualcosa si rompe mentro cerco di leggere
        except:
            raise ExamException ("Errore: Il file è vuoto o non contiene dati validi")
        

    def get_data(self, country= "Italy"):

        # Controllo che il nome del paese sia una stringa
        if not isinstance (country, str):
            raise ExamException ("Il nome del paese deve essere una stringa")
        
        dati = []                       # Lista che conterrà i dati del paese richiesto

        try:
            file = open(self.name, 'r')     # Provo ad aprire il file
            file.readline()                 # Salto l'intestazione (la prima riga del file)
        except:
            raise ExamException ("Errore: impossibile aprire il file")

        # Leggo il file riga per riga
        for riga in file:
            riga = riga.strip()         # Rimuovo spazi bianchi iniziali e finali
            elementi = riga.split(',')  # Divido la riga in base alle virgole

            # Controllo che la riga abbia abbastanza campi
            if len(elementi) < 3:
                continue                # Se non ci sono almeno 4 elementi salto la riga

            data_str = elementi [0]
            # Gestione spazi e case-insensitive per il paese
            paese_row = elementi [2].strip()

            # Se il paese non è quello richiesto salto la riga
            if paese_row.lower () != country.strip().lower():
                continue

            # Controllo che la temperatura sia numerica
            try:
                temperatura = float(elementi[1])
            except:
                continue               # Salto valori non numerici o vuoti

            # Aggiungo il dato valido alla lista dei dati
            dati.append([data_str, temperatura])

        # Chiudo il file
        file.close()

        # Se non ho trovato nessun dato valido per il paese
        if len(dati) == 0:
            raise ExamException ("Errore: Il nome del Paese non è presente nel file")
        
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

def compute_variations(time_series_1, time_series_2, first_year, last_year):
    
    # -------------------
    # 1. CONTROLLI INIZIALI
    # -------------------

    # Controllo sugli anni
    if not isinstance (first_year, int) or not isinstance (last_year, int):
        raise ExamException ("Errore: L'anno inserito non è un intero")
    
    if first_year > last_year:
        raise ExamException ("Intervallo di anni non valido")
    
    # Controllo sulle serie temporali
    if not isinstance(time_series_1, list) or not isinstance (time_series_2, list):
        raise ExamException ("Le serie temporali devono essere liste")
    
    # ---------------------
    # 2. FUNZIONE INTERNA PER CALCOLARE LE MEDIE
    # ---------------------

    # Funzione interna per calcolare media annuali
    def calcola_medie_annuali (time_series):

        # Punto A: Raggruppo tutte le temperature per anno
        dati_per_anno = {}

        for elem in time_series:
            data = elem[0]      # La data è una stringa "YYYY-MM-DD"
            val = elem[1]       # La temperatura è un float

            try:
                # Prendo solo la prima parte del trattino (YYYY) e converto in itero
                anno = int(data.split('-')[0])   
            except:
                continue            # Se la data è scritta male, la ignoro

            # Se è la prima volta che incontro questo anno, creo una lista vuota
            if anno not in dati_per_anno:
                dati_per_anno[anno] = []

            # Aggiungo la temperatura alla lista di quell'anno
            dati_per_anno[anno]. append(val)

        # Punto B: Calcolo la media matematica per ogni anno
        medie = {}
        for anno, lista_valori in dati_per_anno.items():
            # La media si fa solo se la lista non è vuota (per evitare divisioni per zero)
            if len (lista_valori) > 0:
                media = sum(lista_valori) / len(lista_valori)
                medie[anno] = media

        # Ritorno al dizionario pronto con le medie
        return medie
    
    # Punto C: Uso la funzione interna
    medie_1 = calcola_medie_annuali(time_series_1)  # Calcolo le medie della prima serie
    medie_2 = calcola_medie_annuali(time_series_2)  # Calcolo le medie della seconda serie
    
    # ------------------
    # 3. CALCOLO DIFFERENZE TRA LE DUE SERIE
    # -----------------

    variazioni = {}

    # Scorro tutti gli anni nell'intervallo richiesto (incluso gli estremi)
    for anno in range (first_year, last_year + 1):
        # !!! Per calcolare la differenza, l'anno deve esistere in TUTTE E DUE le serie!!!!
        if anno in medie_1 and anno in medie_2:
            differenza = medie_2[anno] - medie_1[anno]
            variazioni[str(anno)] = differenza

    # -----------------
    # 4. CONTROLLO SUL RISULTATO FINALE
    # -----------------

    # Se il dizionario variazioni è vuoto, allora non c'erano anni in comune nell'intervallo.
    if not variazioni:
        raise ExamException("Errore: l'intervallo selezionato non contiene valori validi")

    return variazioni


# ===================================================================================
# CODICE DI TEST 
# ===================================================================================

if __name__ == "__main__":
    print("--- INIZIO TEST ---\n")

    # 1. Creiamo il file CSV finto per il test
    filename_test = "GlobalLandTemperatures_Test.csv"
    csv_content = """dt,AverageTemperature,Country
1900-01-01,10.0,Italy
1900-06-01,20.0,Italy
1900-01-01,12.0,France
1900-06-01,22.0,France
1901-01-01,10.0,Italy
1901-01-01,15.0,France
2000-01-01,5.0,Italy
"""
    try:
        with open(filename_test, "w") as f:
            f.write(csv_content)
        print(f"✅ File '{filename_test}' creato correttamente.\n")
    except Exception as e:
        print(f"❌ Errore creazione file: {e}")

    # 2. Esecuzione Test
    try:
        # Test 1: Lettura Dati
        print("1️⃣  Lettura dati Italia e Francia...")
        f = CSVTimeSeriesFile(filename_test) # Uso la variabile definita qui sopra
        
        dati_ita = f.get_data("Italy")
        print(f"   Dati Italia letti: {len(dati_ita)} righe.")
        
        dati_fra = f.get_data("France")
        print(f"   Dati Francia letti: {len(dati_fra)} righe.")
        print("   ✅ Lettura OK\n")

        # Test 2: Calcolo Variazioni (Matematica)
        print("2️⃣  Calcolo Variazioni (France - Italy)...")
        res = compute_variations(dati_ita, dati_fra, 1900, 1901)
        print(f"   Risultato: {res}")
        
        # Verifica del calcolo per il 1900: (17.0 - 15.0 = 2.0)
        if "1900" in res and abs(res["1900"] - 2.0) < 0.001:
            print("   ✅ Calcolo corretto! (17.0 - 15.0 = 2.0)")
        else:
            print(f"   ❌ Errore di calcolo o chiave mancante.")

        # Test 3: Eccezioni (File vuoto)
        print("\n3️⃣  Test File Vuoto...")
        open("empty_test.csv", "w").close()
        try:
            CSVTimeSeriesFile("empty_test.csv")
            print("   ❌ ERRORE: Doveva scoppiare ma non l'ha fatto!")
        except ExamException as e:
            print(f"   ✅ Eccezione catturata: '{e}'")

        # Test 4: Eccezioni (Paese inesistente)
        print("\n4️⃣  Test Paese Inesistente...")
        try:
            f.get_data("Giappone")
            print("   ❌ ERRORE: Doveva scoppiare per paese mancante!")
        except ExamException as e:
            print(f"   ✅ Eccezione catturata: '{e}'")

    except Exception as e:
        print(f"\n❌ ERRORE IMPREVISTO NEL TEST: {e}")

    print("\n--- FINE TEST ---")