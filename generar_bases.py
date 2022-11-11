import pyodbc, shutil
import numpy as np
from datetime import datetime,date,time
from time import gmtime, strftime,strptime

server = '192.168.1.137'
db_model = 'model.mdb'

nombre_campana = 'afra' 
ciudades=['JUNIN']
numeros = 6000
tabla = 'pywhats2016'

#~ nombre_campana = 'liqui_mach2'
#~ ciudades = ['JUNIN']
#~ numeros = 7000
#~ tabla = 'pywhats2016'

#~ nombre_campana = 'campana_lincoln_II'
#~ ciudades = ['LINCOLN']
#~ numeros = 3500
#~ tabla = 'pywhats2016'

#~ nombre_campana = 'lacasona_zonal_3'
#~ ciudades=['CHACABUCO','LOS TOLDOS','ROJAS','LINCOLN','ARENALES','VEDIA']
#~ numeros = 7000
#~ tabla = 'pywhats'

#~ nombre_campana = 'voices_mujeres_2017' 
#~ ciudades=['CORDOBA']
#~ numeros = 3500
#~ tabla = 'pywhats2016'

#~ nombre_campana = 'encuesta_pirotecnia' 
#~ ciudades=['AMBA','LA PLATA','JUNIN','PERGAMINO','MAR DEL PLATA','BAHIA BLANCA','NECOCHEA','TRENQUE LAUQUEN','AZUL','OLAVARRIA']
#~ numeros = 3500
#~ tabla = 'pywhats'

#~ nombre_campana = 'LN+SP14' 
#~ ciudades=['25 DE MAYO','28 DE NOVIEMBRE','9 DE JULIO','ALEJANDRO KORN','AMERICA','ARRECIFES','AYACUCHO','AZUL','BAHIA BLANCA','BALCARCE','BENITO JUAREZ','BOLIVAR','BRAGADO','CALETA OLIVIA','CAPITAN SARMIENTO','CARHUE','CARLOS CASARES','CARLOS SPEGAZZINI','CARLOS TEJEDOR','CARMEN DE ARECO','CATRIEL','CHACABUCO','CHASCOMUS','CHIVILCOY','CHOELE CHOEL','CHOS MALAL','CINCO SALTOS','COLON','COMODORO RIVADAVIA','CORONEL BRANDSEN','CORONEL DORREGO','CORONEL PRINGLES','CORONEL SUAREZ','CORONEL VIDAL','DAIREAUX','DOLORES','EDUARDO CASTEX','ESQUEL','GENERAL ACHA','GENERAL BELGRANO','GENERAL LAMADRID','GENERAL MADARIAGA','GENERAL PICO','GLEW','GONZALEZ CATAN','GUERNICA','HUINCA RENANCO','JOSE C. PAZ','JUNIN','LAPRIDA','LAS FLORES','LINCOLN','LOBERIA','LOBOS','LOS TOLDOS','LUJAN','LUJAN DE CUYO','MAR DE AJO','MAR DEL PLATA','MARCOS PAZ','MEDANOS','MENDOZA','MERCEDES','MERLO','MIRAMAR','MONTE','MORENO','NAVARRO','NECOCHEA','NEUQUEN','OLAVARRIA','PEHUAJO','PERGAMINO','PILAR','PUERTO DESEADO','PUERTO SANTA CRUZ','PUNTA ALTA','RAUCH','REALICO','RIO GALLEGOS','ROJAS','SALADILLO','SALLIQUELO','SALTO','SAN ANDRES DE GILES','SAN ANTONIO DE ARECO','SAN ANTONIO OESTE','SAN CARLOS DE BARILOCHE','SAN JUAN','SAN LUIS','SAN MARTIN','SAN MARTIN DE LOS ANDES','SAN VICENTE','SANTA ROSA','SANTA TERESITA','SUIPACHA','TANDIL','TRELEW','TRENQUE LAUQUEN','TRES ARROYOS','TRES LOMAS','USHUAIA','VEDIA','VIEDMA']
#~ numeros = 7000
#~ tabla = 'pywhats'

#~ nombre_campana = 'sms_vip_junin' 
#~ numeros = 288
#~ tabla = 'lineas_sms_vip'
#~ like = '2364%'

today  = datetime.now().strftime("%Y-%m-%d")

def lista_de_ciudades(ciudades):
	lista_de_ciudades = '(\''
	for item  in ciudades:
		lista_de_ciudades += item + '\',\''		
	return lista_de_ciudades[:-3]+'\')'

def insert_datos_db(base_i,data,nn):
	MDB = base_i
	DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = 'pw'
	
	# connect to db 
	conn = pyodbc.connect('DRIVER={};DBQ={};PWD={};SERVER=local'.format(DRV,MDB,PWD))
	curr = conn.cursor()
	
	# Se vacia la base por si acaso tuviera datos.
	SQL = 'delete from Client;'
	curr.execute(SQL)
	conn.commit()
	
	cc=numeros*nn
	for i in range(0,np.shape(data)[0]):
		cc+=1
		SQL = 'INSERT INTO Client (`Mobile`,`Data1`) VALUES (%s,%s)' % (data[i][0],cc)
		
		curr.execute(SQL)
		conn.commit()

	curr.close()
	conn.close()


def update_historico(data,campana):
	SQL = 'INSERT INTO historico_enviado (id, mobile, fecha, camp) VALUES '
	for j in range(0,np.shape(data)[0]):
		SQL += " (NULL, '%s', '%s 08:00:00', '%s')," % (data[j][0],today,campana)
	
	SQL = SQL[:-1]+';'
	f = open('test.txt','a')
	f.write(SQL)
	f.close()
	cur.execute(SQL)
	con.commit()




con = pyodbc.connect('Driver={MySQL ODBC 5.3 ANSI Driver};SERVER=%s;DATABASE=dev;UID=maquina;PWD=not' % server)
cur = con.cursor()

SQL = ""
if (tabla == 'lineas_sms_vip'):
	SQL = "SELECT count(*) FROM "+ tabla +" WHERE linea LIKE "+"'"+like+"'"+" AND linea NOT IN (SELECT numero FROM no_llame)"+" AND linea NOT IN (SELECT mobile FROM historico_enviado WHERE camp = '"+nombre_campana+"');"
else:
	SQL = "SELECT count(*) FROM "+ tabla +" WHERE whatsapp = 1 and ciudad IN "+lista_de_ciudades(ciudades)+" AND linea NOT IN (SELECT numero FROM no_llame)"+" AND linea NOT IN (SELECT mobile FROM historico_enviado WHERE camp = '"+nombre_campana+"');"

N_total = np.asarray(cur.execute(SQL).fetchall(), dtype=None, order=None)[0][0]
n = N_total // numeros


print SQL

print 'Hay %s datos para designar. ' % N_total
print 'Tomandolos de a %s se generaran %s bases.' % (numeros,n)
print
print 'Generando bases de datos...'

for i in range(n):
	if (tabla == 'lineas_sms_vip'):
		SQL = "SELECT linea FROM "+ tabla +" WHERE linea LIKE "+"'"+like+"'"+" AND linea NOT IN (SELECT numero FROM no_llame)"+" AND linea NOT IN (SELECT mobile FROM historico_enviado WHERE camp = '"+nombre_campana+"') ORDER BY RAND() LIMIT %s;" % numeros
	else:
		SQL = "SELECT linea FROM "+ tabla +" WHERE whatsapp = 1 and ciudad IN "+lista_de_ciudades(ciudades)+" AND linea NOT IN (SELECT numero FROM no_llame)"+" AND linea NOT IN (SELECT mobile FROM historico_enviado WHERE camp = '"+nombre_campana+"') ORDER BY RAND() LIMIT %s;" % numeros
	print SQL
	
	data = np.asarray(cur.execute(SQL).fetchall(), dtype=None, order=None)
	base_i = '%s-%s_%s.mdb' % (nombre_campana,today,str(i+1) if i>10 else '0'+str(i+1))

	print '%s/%s Base: %s' % (i+1,n,base_i),

	shutil.copy(db_model, base_i)
	print 'Creada.',
	insert_datos_db(base_i,data,i)
	print 'Datos cargados.',
	update_historico(data,nombre_campana)
	print 'Datos en Historico.'
	
cur.close()
con.close()
