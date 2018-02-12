from modelos import Modelos
from os import getenv
from os import system as sys

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