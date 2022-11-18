from time import sleep
import mysql.connector
import pyodbc
import msaccessdb
from getpass import getpass
import os


# Console Clear 
print("\033[H\033[J", end="")


# ------------- Configuracion SQL -------------------

print(" -------- SQL Config Setup -------- ")

mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "",
  database = "dannafox-test"
)


cursor = mydb.cursor()

# ---------------------------------------------------


# Console Clear
print("\033[H\033[J", end="")


files = int(input("Ingrese la cantidad de archivos a crear (1-10): "))

# Check para que se ingrese un numero valido entre el intervalo dado (1 a 10)
while (files > 10 or files < 1):
  print("Numero no valido, ingrese nuevamente")
  files = int(input("Ingrese la cantidad de archivos a crear (1-10): "))


for i in range(files):

  # ------------- Configuracion accdb -----------------

  dir = str(os.getcwd()) + "\File" + str(i) + '.accdb'
  msaccessdb.create(dir)

  db_driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
  conn_str = (rf'DRIVER={db_driver};'
              rf'DBQ={dir};')

  conn = pyodbc.connect(conn_str)

  cursor2 = conn.cursor()
  cursor2.execute("CREATE TABLE numeros(numero STRING);" )
  cursor2.commit()

  #----------------------------------------------------

  total = int(input("Ingrese total de localidades: "))
  
  while (total < 1):
    print("Numero incorrecto, ingrese nuevamente")
    total = int(input("Ingrese total de localidades: "))

  ids = []
  ids_str = "("

    # Conseguir N numeros de la localidad ingresada
  for j in range(total):

    while(True):
      loc = str(input("Ingrese localidad: "))

      # Check para comprobar si la ciudad es correcta
      check = "SELECT nombre,id FROM localidad WHERE nombre = '" + loc + "'"
      cursor.execute(check,)
      if(cursor.fetchone() == None):
        print("No se ha encontrado la localidad, ingrese nuevamente")
      else:
        break


  
    # Conseguir id de las localidades
    getId = "SELECT id FROM localidad WHERE nombre = %s ".format(loc)
    values = (loc,)
    cursor.execute(getId, values)
    id = cursor.fetchone()




    id = int(id[0])

    ids_str += str(id) + ","

  ids_str = ids_str[:-1]
  ids_str += ")" 

  # Seleccionar numeros de las localidades ingresadas

  query = "SELECT numero FROM telefono WHERE localidad_id IN " + ids_str + "ORDER BY RAND() LIMIT 7000"
  cursor.execute(query)



  # Ingresar los numeros al archivo access
  for row in cursor.fetchall():
    cursor2.execute("insert into numeros(numero) values (?)", row)
    cursor2.commit()
          
  print("Carga de numeros completa")
  sleep(3)


# Cierre de conexion
print("Cerrando conexiones...")
cursor.close()
cursor2.close()
sleep(2)


# Console Clear 
print("\033[H\033[J", end="")
print("Finalizado Exitosamente")