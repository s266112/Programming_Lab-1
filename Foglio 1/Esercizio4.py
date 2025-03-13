# Definire una funzione che dati 3 numeri interi stabilisce se possono essere i valori dei lati di un triangolo e se si di che tipo di triangolo

def tipo_triangolo (a, b, c):
     if a + b > c and a + c > b and b + c > a:
          if a == b == c:
               return 'Triangolo Equilatero'
          elif a == b or a == c or b == c:
               return 'Triangolo Isoscele'
          else:
              return "Triangolo scaleno"
     else:
          return "Non è un triangolo"

# Esempi di utilizzo
print(tipo_triangolo(3, 3, 3))  # Triangolo equilatero
print(tipo_triangolo(3, 4, 4))  # Triangolo isoscele
print(tipo_triangolo(3, 4, 5))  # Triangolo scaleno
print(tipo_triangolo(1, 1, 3))  # Non è un triangolo