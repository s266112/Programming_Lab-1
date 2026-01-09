# Creare un oggetto CSV FILE che rappresenti un file CSV, e che:
# a. Venga inizializzato sul nome del file CSV
# b. Abbia un attributo "name" che ne contenga il nome
# c. Abbia un metodo "get_data()" che torni i dati dal file CSV come lista di liste

# IDEA:
# Un oggetto CSVfile rappresenta un file CSV, quindi:
# a. L'oggetto conosce il NOME del file CSV
# b. L'oggetto sa LEGGERE i SUOI DATI


# Definizone della classe
class CSVFile:

    # Costruttore __init__
    def __init__ (self, nome_file):
        self.name = nome_file   # Salvo il nome del file come attributo (self.name -> attributo dell'oggetto)

    # Metodo get_data
    def get_data(self):
        dati = []   # Lista che conterrà i dati del file CSV

        file = open (self.name)   # Apro il file CSV
        file.readline()           # Salto l'intestazione (prima riga)

        for riga in file:               # Per ogni riga del file
            riga = riga.strip()         # Rimuovo spazi bianchi iniziali e finali
            elementi = riga.split(',')  # Divido la riga in elementi separati da virgola
            dati.append(elementi)       # Aggiungo la lista di elementi alla lista dati

    # Chiudo il file
        file.close()

    # Ritorno i dati
        return dati

# Esempio di utilizzo della classe CSFile
mio_file = CSVFile('shampoo_sales.csv')  # Creo un oggetto CSFile
print (mio_file.get_data())              # Stampo i dati del file CSV