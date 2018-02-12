import time

## para configuracoes de zona de tempo, aqui esta sendo usado por default GMT-3
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

	if hora < 0:
		hora += 24
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
	
def getDataHoraAtualFormated():
	values = getDataHoraAtual().split("-")
	return ("%s-%s-%s %s:%s:%s"%(values[0],values[1],values[2],values[3],values[4],values[5]))

def Intervalo(inicio,fim):
	dtini = inicio.split("-")
	dtfim = fim.split("-")

def tratarNome(nome):
	
	caracteres_especiais = [" ","*","$"]
	tratado = ""

	for caracter in nome:
		has_special = False
		for car in caracteres_especiais:
			if caracter == car:
				tratado += "_"
				has_special = True
				break
		if not has_special:
			tratado += caracter
	return tratado

def scheduler():
	print("\n\n    ATENCAO, ESTA FUNCIONALIDADE AINDA NAO FOI IMPEMENTADA,\n   FAVOR CONFIGURAR ROTINAS MANUALMENTE VIA CRONTAB\n   COM O SEGUINTE COMANDO: python3 backup_rotine.py")
	while True:
		op = input(" 1 - diario\n 2 - semanal\n 0 - voltar\n ---> ")
		if op == "0":
			break
		elif op == "1":
			while True:
				try:
					print("a data e hora atual neste sistema é: %s"%getDataHoraAtualFormated())
					hora = input("  insira a hora do backup: (00 - 23 h) -> ")
					hora = int(hora)
					if hora < 0 or hora > 23:
						print("  POR FAVOR, INSIRA UMA HORA VALIDA ")
					else:
						## TODO IMPLEMENTS
						pass
				except:
					print("  POR FAVOR, APENAS NUMEROS ")
					pass
		elif op == "2":
			pass
		else:
			print(" OPCAO INVALIDA ")


