# Scrivete una funzione sum_csv(file_name) che sommi tutti i valori delle vendite degli shampoo del file passato come argomento

def sum_csv(file_name):
    my_file = open(file_name)
    list = []
    line = my_file.readline ()
    while line != '':
        line = line. split (',')
        list.append (line [1])
        line = my_file.readline ()
    my_file.close ()
    somma = sum(list)
    
    return somma
    