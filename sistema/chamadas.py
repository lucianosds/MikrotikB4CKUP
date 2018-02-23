from modelos import Modelos
from os import getenv
from os import system as sys
from sistema import banco

HOMEDIR = getenv("HOME")

def getFTPFile(login):

	chamada = ('lftp -p %s -u %s,%s -e "get %s;quit" %s'%(login.porta,login.usuario,login.senha,login.arquivo,login.ip))
	sys(chamada)

def getSCPFile(login):
	chamada = ('sshpass -p "%s" scp -P %s %s@%s:/%s %s'%(login.senha,login.porta,login.usuario,login.ip,login.arquivo,login.arquivo))
	sys(chamada)

def load_logo():
	
	raw = open("sistema/logo.txt","r")
	readed = raw.readlines()
	for line in readed:
		print (line, end='')
		sys("sleep 0.1")

def createScriptBackup(login):

	ssh = Modelos.SSH(login.ip,login.usuario,login.senha,login.porta)
	ssh.exec_cmd("export file=backup")

def writeToLog(data,logfile):
	raw = open(logfile,"a")
	raw.write(data+"\n")
	raw.close()

def hasPing(host):
	ping_str = "ping -c 1 > /dev/null"
	resposta = sys(ping_str + " " + host)
	return resposta == 0

def addHostKey(host):
	if not (hasKeyBeenConfiguredForThisHost(host)):
		configstring = ("Host %s\n#ADDED BY MIKROTIK BACKUP\n  HostKeyAlgorithms=+ssh-dss\n  KexAlgorithms diffie-hellman-group1-sha1\n"%(host.ip))
		sys("echo '%s' >> ~/.ssh/config" %configstring)
		return True
	else:
		return False

def hasKeyBeenConfiguredForThisHost(host):
	sshconfigfilelines = open(HOMEDIR+"/.ssh/config","r")
	sshconfigfile = sshconfigfilelines.readlines()

	## here we run over all the sshconfig file for verifiry if it have entries
	for index in range(0,len(sshconfigfile)):
		word = sshconfigfile[index].strip("\n").split(" ")

	## here we verify if is an config host entry
		if word[0] == "Host":
	## here we verifify if it matches with our host which we're adding 
			if word[1] == host.ip:
	## here we do a one more advanced check for avoid some issues with an ocasionaly existing config entrie for same host
				markdown = sshconfigfile[index+1].strip("\n")
				if markdown == "#ADDED BY MIKROTIK BACKUP":
					return True
		else:
			pass
	return False

def addHost():		
	nome = ""
	ip = ""
	user = ""
	senha = ""
	protocolo = ""
	porta = 0	

	while True:
		nome = input("\nnome do equipamento -> ")
		if nome != "":
			break
		else:
			sys('echo "$(tput setaf 1)\n  O NOME NAO PODE ESTAR EM BRANCO \n$(tput sgr0)"')
	while True:
		ip = input("IP do equipamento -> ")
		if ip != "":
			break
		else:
			sys('echo "$(tput setaf 1)\n  O IP NAO PODE ESTAR EM BRANCO \n$(tput sgr0)"')
	
	while True:
		user = input("usuario do equipamento -> ")
		if user != "":
			break
		else:
			sys('echo "$(tput setaf 1)\n  O USUARIO NAO PODE ESTAR EM BRANCO \n$(tput sgr0)"')

	while True:
		senha = input("senha do equipamento -> ")
		if senha != "":
			break
		else:
			sys('echo "$(tput setaf 3)\n  DESEJA REALMENTE DEIXAR A SENHA EM BRANCO? \n$(tput sgr0)"')
			op = input(" (Y/N) -> ")
			if op.upper() == "Y":
				break
	while True:
		
		op = input("\nMetodo de backup:\n1 - FTP (via lftp)\n2 - SSH (via scp)\n --> ")

		if op == "1":
			protocolo = "FTP"
			break
		elif op == "2":
			protocolo = "SSH"
			break
		else:
			sys('echo "$(tput setaf 1)\n  OPCAO INVALIDA \n$(tput sgr0)"')

	while True:
		default_port_number = "21"
		if protocolo == "SSH":
			default_port_number = "22"

		try:
			porta = input("porta do equipamento (%s default) -> "%(default_port_number))
			if porta != "":
				porta = int(porta)
			break
		except:
			sys('echo "$(tput setaf 1)\n  POR FAVOR, APENAS DIGITOS \n$(tput sgr0)"')



	new_login = Modelos.Login(utils.tratarNome(nome), ip, user, senha, porta, "backup.rsc",protocolo)
	
	banco.insert(new_login)
	
	sys('echo "$(tput setaf 2)\n  EQUIPAMENTO ADICIONADO COM SUCESSO \n$(tput sgr0)"')

def loadCSV():
	while True:
		tgt = input("   insira o local do arquivo CSV. 0 para cancelar\n --> ")
		if tgt == "0":
			break
		else:
			if path.exists(tgt):
				try:
					banco.loadFromCSVFile(tgt)
				except IndexError:
					sys('echo "$(tput setaf 1)\n  ERRO DURANTE A ANALISE DO ARQUIVO: FORMATO INVALIDO \n$(tput sgr0)"')
				break	
			else:
				sys('echo "$(tput setaf 1)\n  O ARQUIVO NAO EXISTE \n$(tput sgr0)"')

def listar():
	print()

	equipamentos = banco.getAll()
	if len(equipamentos) == 0:
		print("\n Vazio\n")
	else:
		contador = 1
		for equipamento in equipamentos:
			print ("%s - %s"%(contador, equipamento.toString()))
			contador += 1
	print()
