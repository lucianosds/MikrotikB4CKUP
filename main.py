#coding:utf-8
import paramiko
from os import path as path
from os import system as sys
from modelos import Modelos
from sistema import banco, chamadas, utils
	
def main():
	
	chamadas.load_logo()
	
	while True:
		op = input(" 1 - add equipamento\n 2 - listar equipamentos\n 3 - realizar backup\n 4 - sair\n---> ")
		
		if op == "4":
			break
		elif op =="1":
			add()
		elif op == "2":
			listar()
		elif op == "3":
			do_backup()
		else:
			print("\n opcao invalida")
			
def add():
	print()

	nome = ""
	ip = ""
	user = ""
	senha = ""
	protocolo = ""
	porta = 0
	

	while True:
		nome = input("nome do equipamento -> ")
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
		
		op = input("1 - FTP (via lftp)\n2 - SSH (via scp)\n --> ")

		if op == "1":
			protocolo = "FTP"
			break
		elif op == "2":
			protocolo = "SSH"
			break
		else:
			sys('echo "$(tput setaf 1)\n  OPCAO INVALIDA \n$(tput sgr0)"')


	## aqui foi comentado, pois a utilização apenas por Mikrotiks não exige tal parametro

	#arqui = input("backup no equipamento (backup.rsc default) -> ")
	#if arqui == "":
	#	arqui = "backup.rsc"
	
	#if nome == "":
	#	nome = "RB_%s"%ip

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



	new_login = Modelos.Login(nome, ip, user, senha, porta, "backup.rsc",protocolo)
	
	banco.insert(new_login)
	
	sys('echo "$(tput setaf 2)\n  EQUIPAMENTO ADICIONADO COM SUCESSO \n$(tput sgr0)"')
	
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

def do_backup():
	data_atual = utils.getDataAtual()

	logfile = data_atual+".log"
	logpath = ("backups/%s/%s"%(data_atual,logfile))

	if not path.exists("backups"):
		sys("mkdir backups")
	
	if not path.exists("backups/%s"%data_atual):
		sys("mkdir backups/%s"%data_atual)
	
	if path.exists("backups/%s"%logfile):
		sys("rm -R backups/%s/*.log"%(data_atual))
		print(("rm -R backups/%s/%s"%(data_atual,logfile)))
	
	else:
		sys("touch backups/%s/%s"%(data_atual,logfile))
	

	equipamentos = banco.getAll()
	total = len(equipamentos)
	atual = 1
	cont_erro = 0
	cont_ok = 0	


	if len(equipamentos) == 0:

		print("\n NAO EXISTEM EQUIPAMENTOS CADASTRADOS\n")
	
	else:
		
		for equipamento in equipamentos:

			print ("\n verificando conexão com %s(%s)\n "%(equipamento.nome, equipamento.ip))

			if utils.hasPing(equipamento.ip):

				print("\n realizando backup dos equipamentos %s/%s (%s-OK | %s-ERRO) \n"%(atual,total,cont_ok,cont_erro))
				
				if equipamento.protocolo == "FTP":
					chamadas.getFTPFile(equipamento)

				else:

					try:
						chamadas.createScriptBackup(equipamento)
						chamadas.getSCPFile(equipamento)
					except paramiko.ssh_exception.AuthenticationException:
						sys('echo "$(tput setaf 1)  \n  ERRO DE AUTENTICACAO $(tput sgr0)"')
					
				if not path.exists(equipamento.getFileName()):

					sys('echo "$(tput setaf 1)  \n  ERRO $(tput sgr0)"')
					result = "ERRO -> %s"%equipamento.toString()
					chamadas.writeToLog(result,logpath)
					cont_erro += 1

				else:
					arquivo = (equipamento.getFileName())
					nome = data_atual+"_"+equipamento.ip+"_"+equipamento.nome.upper()+".txt"
					sys("mv %s backups/%s/%s"%(arquivo,data_atual,nome))
					sys('echo "$(tput setaf 2)\n  SUCESSO $(tput sgr0)"')
					result = ("%s OK -> %s"%(utils.getDataHoraAtual(),equipamento.toString()))
					chamadas.writeToLog(result,logpath)
					cont_ok +=1
			else:
				sys('echo "$(tput setaf 1)  NÃO FOI POSSIVEL SE CONECTAR (ICMP DOWN) $(tput sgr0)"')
				result = "ERRO -> NÃO FOI POSSIVEL SE CONECTAR (ICMP DOWN) %s"%equipamento.toString()
				chamadas.writeToLog(result,logpath)
				cont_erro += 1
			atual += 1

		print ("\n Rotina de Backups Concluida \n")
		print (" %s backups OK | %s backups ERRO\n"%(cont_ok,cont_erro))
	
if __name__=="__main__":

	main()