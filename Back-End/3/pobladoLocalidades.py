from time import sleep
import pandas as pd
import mysql.connector

# Console Clear
print("\033[H\033[J", end="")


print(" -------- SQL Config Setup -------- ")

mydb = mysql.connector.connect(
  host="localhost",
  user=input("Ingrese nombre de usuario: "),
  password = input("Ingrese contraseña: "),
  database = 'dannafox-test'
)

mycursor = mydb.cursor()

print("\033[H\033[J", end="")

#---------POBLADO DE LOCALIDADES EN LA BASE DE DATOS---------#

# Extraer tabla completa, eliminar bloque y eliminar duplicados
localidades = pd.read_csv('./Back-End/3/rangos.csv')
localidades.pop('BLOQUE')
localidades = localidades.drop_duplicates()  # Dataframe con localidades
localidades.reset_index(drop=True, inplace=True)

# Insertar localidades en base de datos
for i in range(len(localidades)):
    nombre_ins = str(localidades.iloc[i].LOCALIDAD)
    localidad_ins = str(localidades.iloc[i].INDICATIVO)

    sql = "INSERT INTO localidad (nombre, codigo_area) VALUES (%s, %s)"
    values = (nombre_ins, localidad_ins)
    mycursor.execute(sql, values)
    mydb.commit()

print("Se insertaron todas las localidades en la base de datos")

#----------------FIN POBLADO DE LOCALIDADES----------------#