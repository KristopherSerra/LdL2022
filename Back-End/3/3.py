from time import sleep
import pandas as pd
import mysql.connector


# Console Clear
print("\033[H\033[J", end="")


print(" -------- SQL Config Setup -------- ")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dannafox-test"
)

mycursor = mydb.cursor()

print("\033[H\033[J", end="")


# Export del archivo que contiene los rangos
rangos = pd.read_csv('./Back-End/3/rangos.csv')



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

print("Se insertaron las localidades en la base de datos")

#----------------FIN POBLADO DE LOCALIDADES----------------#



# Creacion del DataFrame con la info de la localidad pedida
loc = str(input('Ingrese localidad: ').upper())

# Chequeo para verificar si la ciudad es valida
if (loc in set(rangos["LOCALIDAD"])):
    location = rangos[rangos['LOCALIDAD'] == loc]
else:
    print("No se ha encontrado la localidad ingresada, Finalizando...")
    quit()


# Contienen el conjunto del codigo de area + el bloque
codArea = []
bloque = []

for i in range(len(location)):
    codArea.append(str(location.iloc[i].INDICATIVO))
    bloque.append(str(location.iloc[i].BLOQUE))
print("Datos de la locacion cargados exitosamente")

# Almacena cuantos digitos faltan para completar el numero
faltantes = []
for i in range(len(bloque)):
    faltantes.append(10 - (len(str(codArea[i])) + len(str(bloque[i]))))

print("Se han realizado todos los pre-calculos necesarios")
sleep(3)
print("Iniciando la creacion, aguarde un momento...")


# Crear el numero
numeros = []
for i in range(len(faltantes)):

    start = int(bloque[i])*(10**faltantes[i])
    if (int(bloque[i]) >= 100):
        end = ((int(bloque[i])+1)*(10**faltantes[i]))
    else:
        end = ((int(bloque[i])+10)*(10**faltantes[i]))

    for j in range(start, end):
        sql = "INSERT INTO telefono (nombre, numero) VALUES (%s, %s)".format(
            loc)

        num = str(codArea[i]) + str(j)
        values = (loc, num,)
        mycursor.execute(sql, values)
        mydb.commit()

print("Numeros cargados correctamente, finalizando...")
