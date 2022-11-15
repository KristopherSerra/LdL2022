import openpyxl
from openpyxl import load_workbook
import datetime 
from time import sleep
import mysql.connector



# Console Clear 
print("\033[H\033[J", end="")


# ------------- Configuracion SQL -------------------
print(" -------- SQL Config Setup -------- ")

mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "",
  database = "dannafox-example"
)

print("\033[H\033[J", end="")

cursor = mydb.cursor()
nombre = 'Gibson'#input("Ingrese el nombre de la campaña: ")
# Traer el estado de la campania y comparar
q1 = "SELECT estado FROM campania WHERE nombre = '"+nombre + "'"
cursor.execute(q1,)
estado =  cursor.fetchone()
estado = str(estado[0])
excel = ''
if (estado.upper() != "FINALIZADA" ):
    print("La Campaña no ha finalizado")
    quit()
else:
  #SELECCIONA LA CAMPAÑA FINALIZADA
  q2 = "SELECT * FROM campania WHERE nombre = '" + nombre +"'"
  cursor.execute(q2,)
  info =  cursor.fetchone()
  mensaje = info[5]

q5 = "SELECT nombre FROM localidad l INNER JOIN campania_por_localidad lpc WHERE l.id = lpc.localidad_id AND lpc.campania_id = " + str(info[0])
cursor.execute(q5,)
localidades = cursor.fetchall() #GUARDA LAS LOCALIDADES DE UNA CAMPAÑA

cant_mensajes = info[5] #GUARDA LA CANTIDAD DE MENSAJES DE UNA CAMPAÑA
fecha_inicio = info[6] #GUARDA LA FECHA DE INICIO DE UNA CAMPAÑA

print("\033[H\033[J", end="") #Limpia la pantalla

#Lee el archivo excel con la base de datos
locs = []

for localidad in localidades:
    locs.append(str(localidad))
wb = openpyxl.Workbook()
hoja = wb.active
# Crea la fila del encabezado con los títulos
hoja.append(('Nombre De la Campaña', 'Localidades', 'Cantidad de Mensajes', 'Fecha Inicio'))
producto = [nombre,localidades[0][0],cant_mensajes,fecha_inicio]
hoja.append(producto)

j=0
for a in range(len(localidades)):
  hoja["B"+str(a+2)] = localidades [j][0]
  j = j+1


# producto es una tupla con los valores de un producto 

wb.save('Informe Automatico - Danna Fox.xlsx')


#ENVIO DEL REPORTE VIA GMAIL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
 
# Iniciamos los parámetros del script
remitente = 'labdeleng2022@gmail.com' #GMail creado unicamente para la actividad
destinatarios = ['labdeleng2022@gmail.com']
asunto = '[INFORME] Informe Actualizado de la Campaña publicitaria finalizada'
cuerpo = 'Este es un aviso automatico, por favor no responder.\nAtte. Equipo de Desarrollo - Danna Fox'
ruta_adjunto = 'Informe Automatico - Danna Fox.xlsx'
nombre_adjunto = 'Informe Automatico - Danna Fox.xlsx'

# Creamos el objeto mensaje
mensaje = MIMEMultipart()
 
# Establecemos los atributos del mensaje
mensaje['From'] = remitente
mensaje['To'] = ", ".join(destinatarios)
mensaje['Subject'] = asunto
 
# Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
mensaje.attach(MIMEText(cuerpo, 'plain'))
 
# Abrimos el archivo que vamos a adjuntar
archivo_adjunto = open(ruta_adjunto, 'rb')
 
# Creamos un objeto MIME base
adjunto_MIME = MIMEBase('application', 'octet-stream')
# Y le cargamos el archivo adjunto
adjunto_MIME.set_payload((archivo_adjunto).read())
# Codificamos el objeto en BASE64
encoders.encode_base64(adjunto_MIME)
# Agregamos una cabecera al objeto
adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
# Y finalmente lo agregamos al mensaje
mensaje.attach(adjunto_MIME)
 
# Creamos la conexión con el servidor
sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
 
# Ciframos la conexión
sesion_smtp.starttls()

# Iniciamos sesión en el servidor
sesion_smtp.login('labdeleng2022@gmail.com','qtwxjruajxjrdzor')

# Convertimos el objeto mensaje a texto
texto = mensaje.as_string()

# Enviamos el mensaje
sesion_smtp.sendmail(remitente, destinatarios, texto)

# Cerramos la conexión
sesion_smtp.quit()
print("\n\nSe envio el mail a la direccion LdLenguajes@gmail.com\n\n")
