import pandas as pd
from openpyxl import load_workbook
from openpyxl.chart import BarChart,Reference
import string

informes = pd.read_excel("BDE.xlsx")
tabla_pivote = informes.pivot_table(index="MODALIDAD",columns='OPERADOR', values='BLOQUE')
tabla_pivote.to_excel('Informe Automatico - Danna Fox.xlsx', startrow=1,startcol=1,sheet_name='Octubre 2022')

#Cargar Libro Exce
lectura = load_workbook('Informe Automatico - Danna Fox.xlsx')
pestaña = lectura['Octubre 2022']
min_columna = lectura.active.min_column
max_columna = lectura.active.max_column
min_fila = lectura.active.min_row
max_fila = lectura.active.max_row

#Grafico de Barras
graficoDeBarras = BarChart()
data = Reference(pestaña, min_col=min_columna+1,max_col=max_columna, min_row=min_fila,max_row=max_fila)
categorias = Reference(pestaña, min_col=min_columna,max_col=min_columna, min_row=min_fila+1,max_row=max_fila)

graficoDeBarras.add_data(data, titles_from_data=True)
graficoDeBarras.set_categories(categorias)
graficoDeBarras.title = "Resumen"
graficoDeBarras.y_axis.title = 'Cant. de Usuarios'
graficoDeBarras.x_axis.title = 'Modalidad'
graficoDeBarras.width = 30
graficoDeBarras.height = 15
pestaña.add_chart(graficoDeBarras,"B7")

#Formulas de Excel
pestaña["B5"] = "Recuento"
i="B"
columnas = list(string.ascii_uppercase)
sumas = columnas[0:max_columna]
for i in sumas:
    if i!="U":
        pestaña[f'{i}5'] = f'=SUM({i}3:{i}4'

#Guarda los Cambios Realizados
lectura.save('Informe Automatico - Danna Fox.xlsx')


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
cuerpo = 'Este es un aviso automatico, por favor no responder.\nAtte. Equipo de Desarrollo - Dana Fox'
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
