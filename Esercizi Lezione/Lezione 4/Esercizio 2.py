# Scrivete una classe denominata VEICOLO che disponga di questi attributi dati:
# 1. Modello (per il modello del veicolo);
# 2. Marca (per la marca del veicolo);
# 3. Anno (per l’anno del veicolo);
# 4. Velocità (per la velocità del veicolo)
# E di questi metodi:
# a. __init__: Che accetti come argomenti l’anno, il modello, e la marca. Il metodo dovrebbe inoltre assegnare 0 all’attributo dati velocità.
# b. __str__: Che restituisce una stringa con i dettagli del veicolo (marca, modello, anno e velocità)
# c. Accellerare: Che aggiunge 5 all’attributo dati velocità ogni volta che viene chiamato.
# d. Frenare: Che sottrae 5 dall’attributo dati velocità ogni volta che viene chiamato.
# e. get_speed: Che restituisce la velocità corrente.


## IDEA:
# Una classe Veicolo rappresenta un veicolo, quindi:
# a. La classe conosce il MODELLO, la MARCA, l'ANNO e la VELOCITÀ del veicolo
# b. La classe sa INIZIALIZZARE un veicolo con modello, marca, anno e velocità iniziale 0
# c. La classe sa RAPPRESENTARE un veicolo come stringa


# Definizione della classe Veicolo
class Veicolo:

    # Costruttore __init__
    def __init__ (self, anno, modello, marca):

        # Attributi del veicolo
        self.anno = anno          # Salvo l'ANNO come attributo
        self.modello = modello    # Salvo il MODELLO come attributo
        self.marca = marca        # Salvo la MARCA come attributo
        self.speed = 0            # Inizializzo la velocità iniziale. Self_speed -> E' lo stato dell'oggetto

    # Metodo __str__
    def __str__ (self):

        # Rappresentazione testuale dell'oggetto Veicolo
        return(
            f"Veicolo {self.marca} {self.modello} "
            f"({self.anno}) - Velocità: {self.speed} km/h"  # Serve per poter fare print(veicolo)
        )
    
    # Metodo accelerare
    def accelerare (self):
        self.speed +=5      # Aumenta la velocità di 5

    # Metodo frenare
    def frenare (self):
        self.speed -=5      # Diminuisce la velocità di 5
       
    # Metodo get_speed
    def get_speed (self):
        return self.speed   # Ritorna la velocità corrente
    

# Esempio di utilizzo della classe Veicolo
auto = Veicolo(anno=2020, modello="Panda", marca="Fiat")  # Creo un oggetto Veicolo
print(auto)                       # Stampo la rappresentazione testuale del veicolo

auto.accelerare()                # Chiamo il metodo accelerare
print("Velocità dopo accelerazione:", auto.get_speed())  # Stampo la velocità corrente

auto.frenare()                   # Chiamo il metodo frenare
print("Velocità dopo frenata:", auto.get_speed())        # Stampo la velocità corrente