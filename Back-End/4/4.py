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
  password = input("Ingrese contraseña: ")
)

cursor = mydb.cursor()

# ---------------------------------------------------

# Console Clear
print("\033[H\033[J", end="")


total = int(input("Ingrese total de localidades: "))
loc = []

for i in range(total):
    loc[i] = input("Ingrese localidad ", i+1, " :")



locs = tuple(loc)
query ="SELECT numero FROM numeros WHERE localidad IN ({})".format(locs), " LIMIT %s";
cursor.execute(query,7000)

numero = cursor.fetchall()





# Conexion al archivo Access
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\_mNb\codes\python\LdL2022\Back-End\4\db.accdb;')

print("Conectado a la base de datos")
sleep(2)


cursor = conn.cursor()

#Insert en el archivo
for i in range(len(numero)):
    cursor.execute("INSERT INTO numeros values (?)", numero[i])

# Commit al archivo
conn.commit()

print("Numeros Agregados")

# Cierre de conexion
cursor.close()
conn.close()

print("Finalizado Exitosamente")