#Sebastian Carbone 
#SM3201617
class ExamException(Exception):     #Creo la classe per gestire gli errori
    pass
class CSVTimeSeriesFile:
    def __init__(self,name):        #Creo la classe per gestire il file
        
            self.name=name
            try:                                        #controllo se il file può essere aperto
                with open(self.name,"r") as file: 
                    print("file trovato!")

            except FileNotFoundError:
                raise ExamException("Errore: impossibile aprire il file")
    def get_data(self):
        ris=[]                             #dove salverò il risultato
        with open(self.name,"r") as file:  #apro il file
            for line in file:              #scorro le righe del file
                line=line.strip()
                elements=line.split(",")

                if elements[0]=="dt":      #salto la prima riga e quelle troppo corte
                    continue
                if len(elements)<3:
                    continue
                data = elements[0]                
                temp_media = float(elements[1])
                var_media = float(elements[2])
                if var_media >= 5:           #controllo per ogni riga se la varianzione rispetta le condizioni
                    raise ExamException("Data saltata perchè valore troppo incerto")
                else:
                    ris.append(data, temp_media)    #se le rispetta salvo data e temp_media in ris
        return ris                             #restituisco ris

def compute_month_variation(time_series, first_year, second_year):
    if not isinstance(first_year, int) or not isinstance(second_year,int):              #controllo che first_year e second_year siano interu
        raise ExamException("Errore: gli anni inseriti devono essere di tipo intero.")
    if second_year<=first_year:                                                         #controllo che first_year sia < second_year
        raise ExamException( "Errore: il secondo anno deve essere maggiore del primo.")
    anno1 =[]                                                   #mi serve per salvare le temperature del primo anno
    anno2 =[]                                                   #mi serve per salvare le temperature del secondo anno
    for data, temp in time_series:
        anno = int(data.split("/")[2])
        if anno == first_year:
            if anno not in anno1:
                anno = []
            anno1[anno].append(data,temp)
        elif anno == second_year:
            if anno not in anno2:
                anno = []
            anno2[anno].append(data,temp)
        if len(anno1) == 0 or len(anno2)==0:
            raise ExamException("Gli anni considerati non hanno mesi validi")
        
        mese = int(data.split("/")[1])                            #prendo il mese da ciascuna data
        diff={}                                                   #dove salvo il risultato

        for mese in anno1:
            for mese in anno2:

                if anno1[mese] == anno2[mese]:
                    differenza = anno1[mese[temp]] - anno2[mese[temp]]
                    diff.append(mese,differenza)
                else:
                   continue
                if len(anno1[mese]) == 0 or len(anno2[mese])==0:
                    raise ExamException("La variazione per il mese X non pu`o essere calcolata")
                
    return diff
if __name__ == "__main__":
    file=CSVTimeSeriesFile("Temperatures.csv")
    dati = file.get_data()
    x= compute_month_variation(dati, 1750, 1751)
    print(x)


