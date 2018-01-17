banco = "sistema/database.json"

from modelos import Modelos

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
		raise
		return entradas
