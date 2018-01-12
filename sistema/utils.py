import subprocess
import os, platform
import time

fuso_horario = -3

def getDataAtual():
	ano = time.gmtime().tm_year
	mes = time.gmtime().tm_mon
	dia = time.gmtime().tm_mday
	string_dia = ""
	string_mes = ""
	string_ano = str(ano)

	## validating and formating values

	if dia < 10:
		string_dia = "0"+str(dia)
	else:
		string_dia = str(dia)
	
	if mes < 10:
		string_mes = "0"+str(mes)
	else:
		string_mes = str(mes)

	return ("%s-%s-%s"%(string_ano,string_mes,string_dia))

def getDataHoraAtual():
	hora = time.gmtime().tm_hour + fuso_horario
	minuto = time.gmtime().tm_min
	segundo = time.gmtime().tm_sec

	string_hora = ""
	string_minuto = ""
	string_segundo = ""

	if hora < 10:
		string_hora = "0"+str(hora)
	else:
		string_hora = str(hora)
	
	if minuto < 10:
		string_minuto = "0"+str(minuto)
	else:
		string_minuto = str(minuto)
	
	if segundo < 10:
		string_segundo = "0"+str(segundo)
	else:
		string_segundo = str(segundo)

		return ("%s-%s-%s-%s"%(getDataAtual(),string_hora,string_minuto,string_segundo))

def hasPing(host):

	if  platform.system().lower()=="windows":
		ping_str = "ping -n 1 "
	else:
		ping_str = "ping -c 1 "
	resposta = os.system(ping_str + " " + host)
	return resposta == 0
