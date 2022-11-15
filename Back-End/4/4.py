from time import sleep
import mysql.connector
import pyodbc
import msaccessdb
from getpass import getpass
import os

# funcion para crear una lista
def lista_de_ciudades(ciudades):
	lista_de_ciudades = '(\''
	for item  in ciudades:
		lista_de_ciudades += item + '\',\''		
	return lista_de_ciudades[:-3]+'\')'



# Console Clear 
print("\033[H\033[J", end="")


# ------------- Configuracion SQL -------------------

print(" -------- SQL Config Setup -------- ")

mydb = mysql.connector.connect(
  host = "localhost",
  password = getpass('Ingrese password:'),
  database = "numeros"
  user = "root",
)

cursor = mydb.cursor()

# ---------------------------------------------------


# Console Clear
print("\033[H\033[J", end="")


files = int(input("Ingrese la cantidad de archivos a crear (1-10): "))

if (files > 10 | files < 1):
  print("Numero no valido, cerrando")
  quit()

for i in range(files):

  # ------------- Configuracion accdb -----------------

  dir = str(os.getcwd()) +  str(i) + '.accdb'
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

loc = []
  # Conseguir N numeros de la localidad ingresada
for j in range(total):
      loc[j] = input("Ingrese localidad: ")

query ="SELECT numero FROM telefonos WHERE nombre_localidad IN " + lista_de_ciudades(loc) + " ORDER BY RAND() LIMIT %s ".format(loc)
values = (loc, round(7000))
cursor.execute(query, values,)

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