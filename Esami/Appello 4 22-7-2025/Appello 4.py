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

        # 1. Controllo che il nome del file sia una stringa
        if not isinstance (name, str):
            raise ExamException ("Il nome del file deve essere una stringa")
        
        self.name = name

        # 2. Controllo che il file esista e sia apribile
        try:
            file = open (self.name, 'r')
            file.close()
        except:
            raise ExamException ("Erroe: File non trovato o non apribile")
        
    def get_data (self):

        # Lista che conterrà i dati validi (data, temperatura)
        dati = []

        try:
            file = open(self.name, 'r')         # Provo ad aprire il file
            file.readline()                     # Salto l'intestazione
        except:
            raise ExamException ("Errore: Impossibile aprire il file")
        

        # Leggo il file riga per riga
        for riga in file:
            riga = riga.strip()            # Rimuovo spazi bianchi iniziali e finali
            elementi = riga.split(',')     # Divido la riga in colonne

            # Controllo che ci siano almeno Data e Temperatura
            if len(elementi) < 3:
                continue                   # Se non ci sono almeno 2 elementi salto la riga

            # Estraggo la data (stringa)
            data = elementi [0]

            try:
                # Converto i valori numerici
                temperatura = float(elementi[1])
                incertezza = float(elementi[2])     # IMPORTANTE: Leggo la 3 colonna
            except ValueError:
                continue                        # Se trovo valori vuoti o non numerici, salto la riga)

            # Se il valore è >=5, stampo il messaggio e salto la riga
            if incertezza >=5:
                print ("Data saltata perchè valore troppo incerto")
                continue

            # Se arrivo qui, il dato è valido. Lo salvo
            dati.append([data, temperatura])

        # Chiudo il file
        file.close()

        # Controllo se ho trovato almeno un dato valido
        if len(dati) == 0:
            raise ExamException("Nessun dato valido disponibile")
        
        # Ritorno i dati
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

# ------------
# FUNZIONE compute_month_variation
# ------------
def compute_month_variation (time_series, first_year, second_year):
    
    # --- 1. CONTROLLI INIZIALI ---
    
    # Controllo che gli anni siano interi
    if not isinstance (first_year, int) or not isinstance (second_year, int):
        raise ExamException ("Errore: Gli anni inseriti devono essere di tipo intero")
    
    # Il primo anno deve essere strettamente minore del secondo
    if second_year <= first_year:
        raise ExamException ("Errore: Il secondo anno deve essere maggiore del primo")
    
    # Controllo che la serie temporale sia una lista
    if not isinstance(time_series, list):
        raise ExamException ("Errore: La serie temporale deve essere una lista")
    
    # --- 2. RAGGRUPPAMENTO DATI PER ANNO ---
    
    # Uso 2 dizionari per separare le temperature dei 2 anni scelti
    dati_primo_anno = {}            # Temperatura per il primo anno
    dati_secondo_anno = {}          # Temperatura per il secondo anno

    # Scorro tutta la serie temporale
    for elemento in time_series:
        data_str = elemento [0]     # es: "01/02/19750" (formato DD/MM/YYYY)
        temperatura = elemento [1]

        try:
            # Estraggo Mese e Anno facendo lo split sulla barra '/'
            parti = data_str.split('/')

            # ATTENZIONE: La chiave è di tipo int
            mese = int(parti[1])
            anno = int(parti[2])
        except:
            continue        # Salto date con formato strano

        # Se l'anno corrente è uno dei due che mi interessano, salvo il dato
        if anno == first_year:
            dati_primo_anno[mese] = temperatura
        elif anno == second_year:
            dati_secondo_anno[mese] = temperatura
            
    # --- 3. CALCOLO DIFFERENZE ---
    differenze = {}

    # Scorro tutti i mesi possibili (da 1 a 12)
    for mese in range(1, 13):
        # Verifico se ho il dato per questo mese in entrambi gli anni
        in_primo = mese in dati_primo_anno
        in_secondo = mese in dati_secondo_anno

        if in_primo and in_secondo:
            # Calcolo la variazione (Anno Nuovo - Anno Vecchio)
            diff = dati_secondo_anno[mese] - dati_primo_anno[mese]
            differenze[mese] = diff
        else:
            # Stampo messaggio solo se manca effettivamente in uno dei due anni di riferimento
            if not (in_primo and in_secondo):
                print(f"La variazione per il mese {mese} non può essere calcolata")

        # Se non ho trovato nessuna differenza (dizionario vuoto), lancio eccezione
        if not differenze:
            raise ExamException ("Errore: Nessun mese valido in comune tra i due anni")
    
    # Ritorno il dizionario delle differenze
    return differenze

# ====================
# TEST AUTOMATICO 
# ================
if __name__ == "__main__":
    print("--- INIZIO TEST ---\n")
    
    # 1. Creazione file test
    # Nota: Metto un valore con incertezza ALTA (6.0) per testare il filtro
    csv_content = """dt,LandAverageTemperature,LandAverageTemperatureUncertainty
01/01/1900,10.0,1.0
01/02/1900,12.0,6.0
01/01/2000,15.0,1.0
01/02/2000,14.0,1.0
"""
    # Spiegazione Test:
    # Gennaio: Presente in entrambi (1900 e 2000) e valido. -> Diff: 15.0 - 10.0 = 5.0
    # Febbraio: Nel 1900 ha incertezza 6.0 (>5) -> VIENE SCARTATO.
    #           Quindi Febbraio manca nel 1900 -> Non calcolabile -> Messaggio errore.

    filename = "test_temp.csv"
    try:
        with open(filename, "w") as f:
            f.write(csv_content)

        # Test Lettura
        file = CSVTimeSeriesFile(filename)
        data = file.get_data()
        print(f"Dati letti: {len(data)} (Attesi 3, perché Feb 1900 è scartato)")
        
        # Test Calcolo
        print("\nCalcolo Variazioni (1900 -> 2000):")
        diff = compute_month_variation(data, 1900, 2000)
        print("Risultato:", diff)

        # Verifica
        if 1 in diff and diff[1] == 5.0:
            print("✅ Gennaio OK")
        else:
            print("❌ Errore Gennaio")
            
        if 2 not in diff:
            print("✅ Febbraio correttamente ignorato (scartato in lettura)")
        else:
            print("❌ Errore: Febbraio calcolato ma doveva mancare!")

    except ExamException as e:
        print(f"❌ Errore: {e}")
    except Exception as e:
        print(f"❌ Errore generico: {e}")

    print("\n--- FINE TEST ---")



    
            