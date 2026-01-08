# Scrivete una funzione sum_csv(file_name) che sommi tutti i valori delle vendite degli shampoo del file passato come argomento

def sum_csv(file_name):
    file = open(file_name)

    file.readline()  # Salta l'intestazione
    total = 0.0

    for line in file:
        values = line.split(',')
        total += float(values[1])  # Somma il valore delle vendite (seconda colonna)

        file.close()
        return total

print(sum_csv('shampoo_sales.csv'))  # Esempio di utilizzo    