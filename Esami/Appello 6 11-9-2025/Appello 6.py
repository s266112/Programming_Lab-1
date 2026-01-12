## PARTE 1: LETTURA E FILTRAGGIO DATI (10 PUNTI)
# Scrivere la classe CSVTimeSeriesFile:
# a. La classe deve essere istanziata con il nome del file tramite la variabile name (2 PUNTI).
# b. Deve avere un metodo get_data(country="Italy") che torni una lista di liste, dove il primo elemento è la data (stringa), 
#    il secondo la temperatura media mensile (float) e il terzo incertezza (4 PUNTI)
# c. Scartare le seguenti righe senza lanciare eccezioni (4 PUNTI):
#    - Le righe con valori mancanti/non numerici
#    – Tutte le righe con un paese diverso da quello dato in input
#    – Le righe con incertezza maggiore o uguale di 5 gradi.

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
        
        # 1. Controllo che il nome sia una stringa
        if not isinstance (name, str):
            raise ExamException("Errore: Nome del file non valido")
        
        self.name = name

        # 2. Controllo che il file esista e sia apribile
        try:
            file = open(self.name, 'r')
            linea = file.readline()     # Provo a leggere la prima riga
            file.close()

            # Se la linea è vuota, il file è vuoto
            if not linea:
                raise ExamException("Errore: Impossibile aprire o leggere il file")
            
        except:
            # Catturo sia FileNotFounder che l'errore che ho lanciato io sopra
            raise ExamException("Errore: Impossibile aprire o leggere il file")

    def get_data (self, country="Italy"):

        # Inizializzo la lista dei risultati
        dati = []

        # Flag per verificare se il mpaese esiste nel file (richiesto per l'eccezione finale)
        country_found = False

        try:
            file = open(self.name, 'r')         # Provo ad aprire il file
            file.readline()                     # Salto l'intestazione
        except:
            raise ExamException ("Errore: Impossibile aprire il file")
        

        # Leggo il file riga per riga
        for riga in file:
            riga = riga.strip()            # Rimuovo spazi bianchi iniziali e finali
            elementi = riga.split(';')     # Divido la riga in colonne (IMPORTANTE: punto e virgola)

            # Controllo colonne: dt, Temp, Uncertainty, Country (almeno 4)
            if len(elementi) < 4:
                continue                   # Se non ci sono almeno 4 elementi salto la riga

            # Estraggo i dati grezzi
            data = elementi [0]
            temp_str = elementi[1]
            unc_str = elementi[2]
            country_csv = elementi[3]

            # FILTRO PAESE: In questo caso devo usare case sensitive quindi niente .lower()
            if country_csv != country:
                continue

            # Se arrivo qui, il paese esiste
            country_found = True

            # Converto i valori
            try:
                temperatura = float(temp_str)
                incertezza = float(unc_str)     
            except:
                # In questo caso scarto le righe senza alzare Eccezioni
                continue

            # Le righe con incertezza maggiori o uguali a 5 gradi vanno scartate                       
            if incertezza >=5:
                continue
            
            # Aggiungo alla lista: [data, temperature, incertezza]
            dati.append([data, temperatura, incertezza])

        # Chiudo il file
        file.close()

        # Controllo finale
        if not country_found:
            raise ExamException("Errore: Il paese richiesto non è presente nel file")        
       
        # Ritorno i dati
        return dati


## PARTE 2: CONFRONTO DELLE VARIAZIONI MENSILI CONSECUTIVE TRA DUE PAESI, PER UN CERTO ANNO (10 PUNTI).
# Definire la funzione compute_cons_variation_compare(time series1, time series2, year). La funzione deve:
# a. Raggruppare le misure per anno e mese, estraendo, per ciascun paese, per l’anno dato in input, 
#    la temperatura e l’incertezza del mese; se un mese manca, non `e considerabile (3 PUNTI);
# b. Per ciascun paese, calcolare le variazioni tra mesi consecutivi per le coppie (m, m+1) e 
#    la massima incertezza dove entrambi i mesi sono presenti in entrambi gli anni. (3 PUNTI)
# c. Confrontare le variazioni ottenute calcolando, per ogni coppia (m, m+1), la differenza e l’incertezza totale (2 PUNTI)
# d. Restituire un dizionario con chiave intera m (che rappresenta la coppia (m, m+1)) e la coppia di valori float 
#    della differenza tra le variazioni e dell’incertezza: La chiave m va da 1 a 11. 
#    Considerare solo i m per cui i mesi m e m+1 sono presenti in entrambi gli anni. (2 PUNTI)


## PARTE 3: ECCEZIONE E GESTIONE DEGLI INPUT (10 PUNTI)
# Nelle eccezioni devo gestire i seguenti casi:
# a. Se il file non esiste, `e vuoto o non `e leggibile (2 PUNTI);
# b. Se il country richiesto non compare in alcuna riga valida (2 PUNTI)
# c. year deve essere inserito come tipo intero. (2 PUNTI)
# d. Determinare l’intervallo di anni coperti dai dati in time series. Se year non rientra in tale intervallo, sollevare eccezione (2 PUNTI)
# e. Se non esiste alcuna coppia (m, m+1) valida per il confronto (2 PUNTI)

# ------------
# FUNZIONE compute_variation
# ------------
def compute_variations (time_series, year):
    
    # --- 1. CONTROLLI INIZIALI ---
    
    # Controllo che l'anno sia un intero
    if not isinstance (year, int):
        raise ExamException ("Errore: Anno non valido, deve essere intero")
    
    # Devo trovare l'anno minimo e massimo nel dataset 
    anni_presenti = []

    for riga in time_series:
        data_str = riga[0]     # Formato "MM/YYYY"
        try:
            # Splitto sulla barra '/' e prendo il secondo pezzo (l'anno)
            anno = int(data_str.split('/')[1])
            anni_presenti.append(anno)
        except:
            continue        # Ignoro date strane

        # Se non ho trovato anni validi
        if not anni_presenti:
            raise ExamException ("Errore: Nessun dato valido trovato")
        
        min_year = min(anni_presenti)
        max_year = max(anni_presenti)
    
    # Controllo se l'anno richiesto è dentro il range
    if year < min_year or year > max_year:
        raise ExamException("Errore: L'anno indicato non rientra nella copertura del database")
    
            
    # --- 2. ORGANIZZAZIONE DATI (Per accesso veloce) ---

    # Creo un dizionario: Chiave (Anno, Mese) -> Valore [Temperatura, Incertezza]
    # Questo mi serve per non dover scorrere la lista tante volte.
    dati_organizzati = {}

    for riga in time_series:
        data_str = riga[0]
        temp = riga[1]
        incert = riga[2]

        try:
            parti = data_str.split('/')
            mese = int(parti[0])
            anno = int(parti[1])

            dati_organizzati[(anno, mese)] = [temp, incert]
        except:
            continue

    # --- 3. CALCOLO MATEMATICO (Ciclo sui mesi) ---

    risultati = {}

    year1 = year
    year2 = year + 1

    # Cislo sui mesi da 1 a 11 (perchè la formula usa m e m+1)
    for m in range(1,12):
        m_next = m + 1

        # Verifico se ho i dati per l'Anno 1 (mase corrente e successivo)
        ha_dati_y1 = (year1, m) in dati_organizzati and (year1, m_next) in dati_organizzati

        # Verifico se ho i dati per l'Anno 2 (mese corrente e successivo)
        ha_dati_y2 = (year2, m) in dati_organizzati and (year2, m_next) in dati_organizzati

        # Se ho TUTTI i dati necessari, procedo al calcolo
        if ha_dati_y1 and ha_dati_y2:

            # Recupero dati Anno 1
            t1_m = dati_organizzati[(year1, m)] [0]
            t1_next = dati_organizzati[(year1, m_next)] [0]
            unc1_m = dati_organizzati[(year1, m)][1]
            
            # Recupero dati Anno 2
            t2_m = dati_organizzati[(year2, m)][0]
            t2_next = dati_organizzati[(year2, m_next)][0]
            unc2_m = dati_organizzati[(year2, m)][1] 

            # A. Calcolo Variazione 
            delta1 = t1_next - t1_m     # Serie 1 (Temp successiva - Temp attuale)
            delta2 = t2_next - t2_m     # Serie 2 (Temp successiva - Temp attuale)
            
            # B. Differenza delle Variazioni (Richiesta del testo)
            diff_variazioni = delta2 - delta1
            
            # C. Incertezza Totale (Somma delle incertezze dei mesi m)
            incertezza_totale = unc1_m + unc2_m
            
            # Salvo nel dizionario: Chiave m -> [differenza, incertezza]
            risultati[m] = [diff_variazioni, incertezza_totale]

    # --- 4. CONTROLLO FINALE ---
    # Se il dizionario risultati è vuoto, significa che non c'erano dati sufficienti
    if not risultati:
        raise ExamException("Errore: dati insufficienti per calcolare le variazioni")

    return risultati

# ===================================================================================
# TEST AUTOMATICO (Da incollare alla fine)
# ===================================================================================
if __name__ == "__main__":
    print("--- INIZIO TEST ---\n")
    
    # 1. Creazione file CSV finto (Nota il separatore ;)
    csv_content = """dt;AverageTemperature;AverageTemperatureUncertainty;Country
01/2000;10.0;0.1;Italy
02/2000;12.0;0.1;Italy
01/2001;15.0;0.2;Italy
02/2001;18.0;0.2;Italy
"""
    # LOGICA DEL TEST:
    # Anno 2000 (Gen->Feb): da 10 a 12 -> Variazione = +2
    # Anno 2001 (Gen->Feb): da 15 a 18 -> Variazione = +3
    # Differenza Variazioni: 3 - 2 = 1.0
    # Incertezza Totale (Gen 2000 + Gen 2001): 0.1 + 0.2 = 0.3

    filename = "test_appello6.csv"
    
    try:
        with open(filename, "w") as f:
            f.write(csv_content)

        # Test Lettura
        print("1️⃣  Lettura file...")
        ts = CSVTimeSeriesFile(filename)
        data = ts.get_data("Italy")
        print(f"   Dati letti: {len(data)} (Attesi 4)")
        
        # Test Calcolo
        print("\n2️⃣  Calcolo Variazioni (2000 vs 2001)...")
        res = compute_variations(data, 2000)
        print(f"   Risultato: {res}")
        
        # Verifica matematica
        if 1 in res:
            diff, unc = res[1]
            # Uso abs() < 0.001 per confrontare i float senza errori di arrotondamento
            if abs(diff - 1.0) < 0.001 and abs(unc - 0.3) < 0.001:
                print("   ✅ CALCOLO CORRETTO! (Diff=1.0, Unc=0.3)")
            else:
                print(f"   ❌ Errore valori: Diff={diff}, Unc={unc}")
        else:
            print("   ❌ Errore: Mese 1 mancante nei risultati")

    except ExamException as e:
        print(f"❌ Errore ExamException: {e}")
    except Exception as e:
        print(f"❌ Errore Generico: {e}")

    print("\n--- FINE TEST ---")