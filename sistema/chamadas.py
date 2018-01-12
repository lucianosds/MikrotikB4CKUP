from modelos import Modelos
from os import system as sys


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
