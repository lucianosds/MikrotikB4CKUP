#coding:utf-8

import paramiko
from os import path as path
from os import system as sys
from modelos import Modelos
from sistema import banco, chamadas, utils

def main():
	
	chamadas.load_logo()

	while True:
		
		op = input(" 1 - add equipamento\n 2 - listar equipamentos\n 3 - realizar backup\n 0 - sair\n---> ")
		
		if op == "0":
			break
		elif op =="1":
			add()
		elif op == "2":
			listar()
		elif op == "3":
			do_backup()
		elif op == "4":
			utils.scheduler()
		else:
			print("\n opcao invalida")
		print()
			
def add():
	while True:
		op = input("  1 - inserir host\n  2 - carregar de arquivo CSV\n  0 - voltar\n --> ")
		if op == "0":
			break
		elif op == "2":
			loadCSV()
			break
		elif op == "1":
			addHost()
			break

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

def do_backup(quiet=False):

	data_atual = utils.getDataAtual()

	logfile = data_atual+".log"
	logpath = ("backups/%s/%s"%(data_atual,logfile))

		## aqui e verifica a configuracao do SSH
	if ("cat ~/.ssh/known_hosts" != 0):
		sys("touch ~/.ssh/known_hosts")
	if ("cat ~/.ssh/config" != 0):
		sys("touch ~/.ssh/config")

		## aqui e verificada a existencia e criacao dos arquivos log
	if not path.exists("backups"):
		sys("mkdir backups")
	
	if not path.exists("backups/%s"%data_atual):
		sys("mkdir backups/%s"%data_atual)
	
	if not path.exists("backups/%s"%logfile):
		sys("touch backups/%s/%s"%(data_atual,logfile))
	

	equipamentos = banco.getAll()
	total = len(equipamentos)
	atual = 1
	cont_erro = 0
	cont_ok = 0	
	tempo_inicio = utils.getDataHoraAtualFormated()
	tempo_fim = ""

	if len(equipamentos) == 0:
		if not quiet:
			sys('echo "$(tput setaf 1)  \n  NAO EXISTEM EQUIPAMENTOS CADASTRADOS $(tput sgr0)\n\n"')
		chamadas.writeToLog("\n\n############################# ROTINA DE BACKUPS INICIADA #############################",logpath)
		chamadas.writeToLog("\n############################# %s #############################\n"%tempo_inicio,logpath)
		chamadas.writeToLog("\n 		ERRO: NAO EXISTEM EQUIPAMENTOS CADASTRADOS",logpath)	
	else:

		if not quiet:
			sys('echo "$(tput setaf 6)      INICIALIZANDO ROTINA DE BACKUPS $(tput sgr0)\n\n\n"')
			sys("sleep 1")


		chamadas.writeToLog("\n\n############################# ROTINA DE BACKUPS INICIADA #############################",logpath)
		chamadas.writeToLog("\n############################# %s #############################\n"%tempo_inicio,logpath)
		
		for equipamento in equipamentos:
			sys("sleep 2")
			has_added_an_new_entry = chamadas.addHostKey(equipamento)
			if not quiet:
				print("#"*100)
				print("\n  TENTANDO BACKUP DO EQUIPAMENTO %s/%s (%s-OK | %s-ERRO) "%(atual,total,cont_ok,cont_erro))
				sys('echo "$(tput setaf 4)\n  VERIFICANDO ENTRADAS DE CHAVE SSH... $(tput sgr0)"')
				if not has_added_an_new_entry:
					sys('echo "$(tput setaf 2)  OK... \n$(tput sgr0)"')	
				else:
					sys('echo "$(tput setaf 3)  NAO ENCONTRADA, ADICIONANDO... $(tput sgr0)"')
					sys('echo "$(tput setaf 2)  CHAVE ADICIONADA... \n$(tput sgr0)"')
				sys('echo "$(tput setaf 3)\n verificando conexão com %s(%s)  $(tput sgr0)"'%(equipamento.nome, equipamento.ip))
			if chamadas.hasPing(equipamento.ip):
				if not quiet:
					sys('echo "$(tput setaf 2) resposta de Ping OK $(tput sgr0)"')
					sys('echo "$(tput setaf 2)  tentando se conectar ao equipamento... $(tput sgr0)"')
					
				EXPECTED_ERROR = "None"

				if equipamento.protocolo == "FTP":
					try:

						chamadas.getFTPFile(equipamento)
					
					except:
						raise
						cont_erro+=1

					if EXPECTED_ERROR == "None":

						if not path.exists(equipamento.getFileName()):
							if not quiet:
								sys('echo "$(tput setaf 1)  \n  ERRO $(tput sgr0)"')
							result = ("%s |ERRO| -> ERRO DE FTP %s"%(utils.getDataHoraAtualFormated(), equipamento.toStringLog()))
							chamadas.writeToLog(result,logpath)
							cont_erro += 1

						else:
							arquivo = (equipamento.getFileName())
							nome = data_atual+"_"+equipamento.ip+"_"+equipamento.nome.upper()+".txt"
							sys("mv %s backups/%s/%s"%(arquivo,data_atual,nome))
							if not quiet:
								sys('echo "$(tput setaf 2)\n  SUCESSO $(tput sgr0)"')
							result = ("%s |OK  | -> %s"%(utils.getDataHoraAtualFormated(),equipamento.toStringLog()))
							chamadas.writeToLog(result,logpath)
							cont_ok +=1
					else:
						result = ("%s |ERRO| -> %s %s"%(utils.getDataHoraAtualFormated(),EXPECTED_ERROR, equipamento.toStringLog()))
						chamadas.writeToLog(result,logpath)
						cont_erro += 1
					
				
				else:

					try:
						
						chamadas.createScriptBackup(equipamento)
						chamadas.getSCPFile(equipamento)
					
					except paramiko.ssh_exception.AuthenticationException:
						if not quiet:
							sys('echo "$(tput setaf 1)  \n  ERRO DE AUTENTICACAO (Usuario e/ou senha corretos? ) $(tput sgr0)"')
						EXPECTED_ERROR = "ERROR DE AUTENTICACAO"

					except paramiko.ssh_exception.NoValidConnectionsError:
						if not quiet:
							sys('echo "$(tput setaf 1)  \n  CONEXAO RECUSADA (o ssh esta em execucao e na porta correta? ) $(tput sgr0)"')
						EXPECTED_ERROR = "CONEXAO RECUSADA"

					except TimeoutError:
						if not quiet:
							sys('echo "$:(tput setaf 1)  \n  TEMPO DE CONEXAO ESGOTADO (o equipamento esta online e/ou possui regra de firewall para ICMP? ) $(tput sgr0)"')
						EXPECTED_ERROR = "TEMPO DE CONEXAO ESGOTADO"

					except paramiko.ssh_exception.SSHException:
						if not quiet:
							sys('echo "$:(tput setaf 1)  \n  CONEXAO RECUSADA PARA ESTE HOST (o equipamento esta com regra de firewall ativa? )$(tput sgr0)"')
						EXPECTED_ERROR = "CONEXAO RECUSADA PARA ESTE HOST"

					except EOFError:
						if not quiet:
							sys('echo "$:(tput setaf 1)  \n  ERRO DURANTE O PROCESSAMENTO DA CONEXAO $(tput sgr0)"')
						EXPECTED_ERROR = "ERRO DURANTE A MANIPULACAO DA CONEXAO"
					except:
						pass

					if EXPECTED_ERROR == "None":

						if not path.exists(equipamento.getFileName()):
							if not quiet:
								sys('echo "$(tput setaf 1)  \n  ERRO $(tput sgr0)"')
							result = ("%s |ERRO| -> ERRO DURANTE O BACKUP DO EQUIPAMENTO %s"%(utils.getDataHoraAtualFormated(), equipamento.toStringLog()))
							chamadas.writeToLog(result,logpath)
							cont_erro += 1

						else:
							arquivo = (equipamento.getFileName())
							nome = data_atual+"_"+equipamento.ip+"_"+equipamento.nome.upper()+".txt"
							sys("mv %s backups/%s/%s"%(arquivo,data_atual,nome))
							if not quiet:
								sys('echo "$(tput setaf 2)\n  BACKUP REALIZADO COM SUCESSO $(tput sgr0)"')
							result = ("%s |OK  | -> %s"%(utils.getDataHoraAtualFormated(),equipamento.toStringLog()))
							chamadas.writeToLog(result,logpath)
							cont_ok +=1
					else:
						result = ("%s |ERRO| -> %s %s"%(utils.getDataHoraAtualFormated(),EXPECTED_ERROR, equipamento.toStringLog()))
						chamadas.writeToLog(result,logpath)
						cont_erro += 1
						
			else:
				if not quiet:
					sys('echo "$(tput setaf 1)\n  NÃO FOI POSSIVEL SE CONECTAR \n(o endereco esta correto, equipamento esta online e/ou possui regras de firewall? ) $(tput sgr0)"')
				result = ("%s |ERRO| -> SEM RESPOSTA DO HOST (ICMP DOWN) %s"%(utils.getDataHoraAtualFormated(),equipamento.toStringLog()))
				chamadas.writeToLog(result,logpath)
				cont_erro += 1
			atual += 1
		tempo_fim = utils.getDataHoraAtualFormated()

		chamadas.writeToLog("\n############################# ROTINA DE BACKUPS CONCLUIDA #############################\n",logpath)
		chamadas.writeToLog("############################# %s #############################\n"%tempo_fim,logpath)
		chamadas.writeToLog("######################### %s backups OK | %s backups ERRO #############################\n"%(cont_ok,cont_erro),logpath)
			
		if not quiet:
			print ("\n Rotina de Backups Concluida \n")
			print ("%s backups OK | %s backups ERRO \n"%(cont_ok,cont_erro))



if __name__=="__main__":

	main()