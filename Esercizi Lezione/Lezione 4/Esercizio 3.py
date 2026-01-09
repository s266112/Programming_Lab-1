# a. Crea una sottoclasse auto che ha in aggiunta l'attributo numero_porte ecambia il metodo _str__ di conseguenza
# b.Crea una sottoclasse moto che ha in aggiunta l'attributo tipo (ad esempio,"Sportiva" o "Touring") e cambia il metodo _str__ di conseguenza

# IDEA: Auto e Moto sono tipi di Veicolo, quindi:
# a. Auto e Moto ereditano da Veicolo


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
    
## Sottoclasse AUTO

class Auto(Veicolo):

    """
    Classe Auto, sottoclasse di Veicolo.
    Aggiunge l'attributo numero_porte.
    """

    def __init__(self, anno, modello, marca, numero_porte):
            # Inizializzo la parte veicolo usando il costruttore della superclasse
            super().__init__(anno, modello, marca)

            # Attributo specifico dell'auto
            self.numero_porte = numero_porte

    def __str__(self):
        # Rappresentazione testuale dell'oggetto Auto
        return (
            f"Auto {self.marca} {self.modello} "
            f"({self.anno}) - Porte: {self.numero_porte} "
            f" - Velocità: {self.speed} km/h"
        )

## Sottoclasse MOTO

class Moto(Veicolo):

    """
    Classe Moto, sottoclasse di Veicolo.
    Aggiunge l'attributo tipo.
    """

    def __init__(self, marca, modello, anno, tipo):
        # Inizializzo la parte veicolo usando il costruttore della superclasse
        super().__init__(anno, modello, marca)

        # Attributo specifico della moto
        self.tipo = tipo

    def __str__(self):
        # Rappresentazione testuale dell'oggetto Moto
        return (
            f"Moto {self.marca} {self.modello} "
            f"({self.anno}) - Tipo: {self.tipo} "
            f" - Velocità: {self.speed} km/h"
        )
            
# Esempio di utilizzo della classe Veicolo, Auto e Moto
auto = Auto(anno=2021, modello="Panda", marca="Fiat", numero_porte=4)  # Creo un oggetto Auto
moto = Moto(anno=2020, modello="R1", marca="Yamaha", tipo="Sportiva")  # Creo un oggetto Moto
print(auto)                      # Stampo la rappresentazione testuale dell'auto
print(moto)                      # Stampo la rappresentazione testuale della moto

auto.accelerare()                # Chiamo il metodo accelerare sull'auto
moto.accelerare()                # Chiamo il metodo accelerare sulla moto

print("Velocità auto dopo accelerazione:", auto.get_speed())  # Stampo la velocità corrente dell'auto
print("Velocità moto dopo accelerazione:", moto.get_speed())  # Stampo la velocità corrente della moto
