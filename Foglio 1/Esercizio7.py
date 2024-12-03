# Scrivere una funzione che prende in input due liste e ritorna `True` se le due liste hanno almeno un elemento in comune, altrimenti ritorna `False.

def confronto (lista1, lista2):     # Ciclo for per confrontare gli elementi delle due liste
    for elemento in lista1:         # Ciclo for per ogni elemento della prima lista 
        if elemento in lista2:      # Ciclo for per ogni elemento della seconda lista
            return True             
    return False                    
    
list1 = [1, 2, 3, 4]
list2 = [4, 6, 7, 8]
print (confronto (list1, list2)) 