import os
import paramiko
from paramiko import SSHClient


class SSH:
	def __init__(self,host="",user="",senha="",porta=22):
		self.ssh = SSHClient()
		## this method has been depreciated
		#self.ssh.load_system_host_keys()
		self.ssh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(hostname=host,username=user,password=senha,port=porta)

	def exec_cmd(self,cmd):
		stdin,stdout,stderr = self.ssh.exec_command(cmd)
		if stderr.channel.recv_exit_status() != 0:
			print (stderr.read())
		else:
			##print stdout.read()
			## so sucesso
			pass

class Login():
	def __init__(self,nome="",ip="",usuario="",senha="",porta=2227,arquivo="backup.rsc",protocolo = ""):
		self.nome = nome
		self.ip = ip
		self.usuario = usuario
		self.senha = senha
		self.protocolo = protocolo

		if protocolo == "SSH" and porta == "":
			self.porta = 22
		elif self.protocolo == "FTP" and porta == "":
			self.porta = 21
		else:
			self.porta = porta
		self.arquivo = arquivo
		

	def toJSON(self):
		return ('{"nome":"%s","ip":"%s","usuario":"%s","senha":"%s","porta":"%s","arquivo":"%s","protocolo":"%s"}'%(self.nome,self.ip,self.usuario,self.senha,self.porta,self.arquivo,self.protocolo))
	
	def fromJSON(json):
		d =  eval(json)
		return Login(d["nome"], d["ip"], d["usuario"], d["senha"], int(d["porta"]), d["arquivo"],d["protocolo"])
	
	def toString(self):
		return ('nome:%s|ip:%s|usuario:%s|senha:%s|porta:%s|protocolo:%s|arquivo_backup:%s' %(self.nome,self.ip,self.usuario,self.senha,self.porta,self.protocolo,self.arquivo))
	
	def toStringLog(self):
		return ('nome:%s | ip: %s'%(self.nome,self.ip))

	def getFileName(self):
		if self.arquivo.split("/").pop() != None:
			return self.arquivo.split("/").pop()
		else:
			return arquivo
		
