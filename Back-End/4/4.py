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
  user = input("Ingrese nombre de usuario: "),
  password = getpass('Ingrese password:'),
  database = "numeros"
)

cursor = mydb.cursor()

# ---------------------------------------------------


# Console Clear
print("\033[H\033[J", end="")

# Check para no crear mas de 10 archivos
for i in range(10):

  # ------------- Configuracion accdb -----------------

  dir = str(os.getcwd()) + '\Back-End\Access\File_' + str(i) + '.accdb'
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


  # Conseguir N numeros de la localidad ingresada
  for i in range(total):
      loc = input("Ingrese localidad: ")
      query ="SELECT numero FROM telefonos WHERE nombre_localidad = %s ORDER BY RAND() LIMIT %s ".format(loc)
      values = (loc, round(7000/total))
      cursor.execute(query, values,)

      # Ingresar los numeros al archivo access
      for row in cursor.fetchall():
        cursor2.execute("insert into numeros(numero) values (?)", row)
        cursor2.commit()
        
  print("Carga de numeros completa")
  sleep(3)

  if(i < 9):
    x = input("Desea crear otro archivo Access? (s para continuar, cualquier otra tecla para cancelar): ")
    if(x.lower() != 's'):
      break;

# Cierre de conexion
print("Cerrando conexiones...")
cursor.close()
cursor2.close()
sleep(2)


# Console Clear 
print("\033[H\033[J", end="")
print("Finalizado Exitosamente")