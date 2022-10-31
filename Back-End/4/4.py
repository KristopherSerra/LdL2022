from time import sleep
import mysql.connector
import pyodbc


# Console Clear 
print("\033[H\033[J", end="")


# ------------- Configuracion SQL -------------------

print(" -------- SQL Config Setup -------- ")

mydb = mysql.connector.connect(
  host="localhost",
  user=input("Ingrese nombre de usuario: "),
  password = input("Ingrese contraseña: "),
  database = "numeros"
)

cursor = mydb.cursor()

# ---------------------------------------------------

# ------------- Configuracion accdb -----------------

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ= C:\Users\_mNb\codes\python\LdL2022\Back-End\4\db.accdb;')
cursor2 = conn.cursor()

#----------------------------------------------------

# Console Clear
print("\033[H\033[J", end="")


total = int(input("Ingrese total de localidades: "))


# Conseguir N numeros de la localidad ingresada
for i in range(total):
    loc = input("Ingrese localidad: ")
    query ="SELECT numero FROM telefonos WHERE nombre_localidad = %s LIMIT %s".format(loc)
    values = (loc, round(7000/total))
    cursor.execute(query, values,)


# Ingresar los numeros al archivo access
for row in cursor.fetchall():
  cursor2.execute("insert into numeros(numero) values (?)", row)
  cursor2.commit()


# Cierre de conexion
cursor.close()
cursor2.close()

print("Finalizado Exitosamente")