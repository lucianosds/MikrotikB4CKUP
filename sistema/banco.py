banco = "sistema/database.json"

from modelos import Modelos
from sistema import utils

def insert(data):
	try:
		db = open(banco,"a")
		db.write(data.toJSON()+"\n")
		db.close()
	except:
		raise
	
def getAll():
	entradas = []
	try:
		entradas = []
		db = open(banco,"r")
		base = db.readlines()
		for linha in base:
			entradas.append(Modelos.Login.fromJSON(linha))
		db.close()
		return entradas
	except:
		return entradas

def loadFromCSVFile(tgt):
	opened_file = open(tgt,"r")
	lines = opened_file.readlines()
	TOTAL = len(lines)
	ATUAL = 1
	for l in lines:
		line = l.split(",")
		modelo = Modelos.Login(utils.tratarNome(line[0]),line[1],line[2],line[3],line[4],line[5],line[6].strip("\n"))
		print("inserindo entrada: %s/%s"%(ATUAL,TOTAL))
		insert(modelo)
		ATUAL += 1
	print("\n\n    FEITO\n\n")

def addHostKey(host):
	hkstring = ("Host %s\n  HostName %s\n  HostKeyAlgorithms=+ssh-dss"%(host.nome, host.ip ))
	print (hkstring)