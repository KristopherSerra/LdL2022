from time import sleep
import pandas as pd
import mysql.connector
import os

# Console Clear
print("\033[H\033[J", end="")



print(" -------- SQL Config Setup -------- ")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password = "",
  database = "dannafox-test"
)

mycursor = mydb.cursor()

print("\033[H\033[J", end="")


#Export del archivo que contiene los rangos
dir = str(os.getcwd()) + '\Rangos.csv'
rangos = pd.read_csv(dir)

while True:
    try:
        cantidad = int(input("Ingrese total de localidades a cargar: "))
        while (cantidad < 1):
            print("Numero no valido, ingrese nuevamente...")
            cantidad = int(input("Ingrese total de localidades a cargar: "))
        break
    except ValueError:
        print("Solo numeros,intente nuevamente.")

# Check para que se ingrese 1 localidad como minimo
while (cantidad < 1):
    print("Numero no valido, ingrese nuevamente...")
    cantidad = int(input("Ingrese total de localidades a cargar: "))


for i in range(cantidad):
    # Creacion del DataFrame con la info de la localidad pedida
    loc = str(input('Ingrese localidad: ').upper())

    query = "SELECT nombre FROM localidad WHERE nombre = '" + loc + "'"
    mycursor.execute(query,)

    while (mycursor.fetchone() != None):
        print("La localidad ya ha sido cargada, ingrese nuevamente")
        loc = str(input('Ingrese localidad: ').upper())
        query = "SELECT nombre FROM localidad WHERE nombre = '" + loc + "'"
        mycursor.execute(query,)

    # Chequeo para verificar si la ciudad es valida
    while(loc not in set(rangos["LOCALIDAD"])):
        print("No se ha encontrado la localidad ingresada, ingrese nuevamente...")
        loc = str(input('Ingrese localidad: ').upper())
        
    location = rangos[rangos['LOCALIDAD'] == loc]
  
    cod = str(location.iloc[0].INDICATIVO)

    sql = "INSERT INTO localidad (nombre, codigo_area) VALUES (%s, %s)"
    values = (loc, cod)
    mycursor.execute(sql, values)
    mydb.commit()

    print("Se insertaron los datos de la localidad en la base de datos")
    sleep(2)
    print("\033[H\033[J", end="")

    # Obtener id de la localidad
    getId = "SELECT id FROM localidad WHERE nombre = %s ".format(loc)
    values = (loc,)
    mycursor.execute(getId, values)
    id = mycursor.fetchone()
    id = int(id[0])



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
            sql = "INSERT INTO telefono (localidad_id, nombre, numero) VALUES (%s, %s, %s)".format(id)

            num = str(codArea[i]) + str(j)
            values = (id, loc, num,)
            mycursor.execute(sql, values)
            mydb.commit()

    print("Numeros cargados correctamente")


