#contadoring:utf-8
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
	
	nome = input("nome do equipamento -> ")
	ip = input("IP do equipamento -> ")
	user = input("usuario do equipamento -> ")
	senha = input("senha do usuario -> ")
	porta = 0
	
	while True:
		try:
			porta = input("porta do equipamento (2227 default) -> ")
			if porta != "":
				porta = int(porta)
			break
		except:
			print("\n  Por Favor, Apenas Digitos\n")

	## aqui foi comentado, pois a utilização apenas por Mikrotiks não exige tal parametro

	#arqui = input("backup no equipamento (backup.rsc default) -> ")
	#if arqui == "":
	#	arqui = "backup.rsc"
	
	#if nome == "":
	#	nome = "RB_%s"%ip

	banco.insert(Modelos.Login(nome, ip, user, senha, porta, "backup.rsc"))
	
	print ("\n EQUIPAMENTO ADICIONADO COM SUCESSO\n")
	
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
				
				chamadas.createScriptBackup(equipamento)
				
				if equipamento.porta == 21:
					chamadas.getFTPFile(equipamento)
				else:
					chamadas.getSCPFile(equipamento)
					
				if not path.exists(equipamento.getFileName()):

					sys('echo "$(tput setaf 1)  ERRO $(tput sgr0)"')
					result = "ERRO -> %s"%equipamento.toString()
					chamadas.writeToLog(result,logpath)
					cont_erro += 1

				else:
					arquivo = (equipamento.getFileName())
					nome = data_atual+"_"+equipamento.ip+"_"+equipamento.nome.upper()+".txt"
					sys("mv %s backups/%s/%s"%(arquivo,data_atual,nome))
					sys('echo "$(tput setaf 2)  SUCESSO $(tput sgr0)"')
					result = ("%s OK -> %s"%(utils.getDataHoraAtual(),equipamento.toString()))
					chamadas.writeToLog(result,logpath)
					cont_ok +=1
				atual+= 1
			else:
				sys('echo "$(tput setaf 1)  NÃO FOI POSSIVEL SE CONECTAR (ICMP DOWN) $(tput sgr0)"')
				result = "ERRO -> NÃO FOI POSSIVEL SE CONECTAR (ICMP DOWN) %s"%equipamento.toString()
				chamadas.writeToLog(result,logpath)
				cont_erro += 1

		print ("\n Rotina de Backups Concluida \n")
		print (" %s backups OK | %s backups ERRO\n"%(cont_ok,cont_erro))
	
if __name__=="__main__":













	main()
