# MIKROTIK B4CKUP
#
#
#
 ### MIKROTIK BACKUP é um conjunto de scripts escritos em Python e Shell, que permitem o backup automático das configurações de equipamentos Mikrotik.
 ### Útil para aqueles que administram redes e necessitam manter backups de seus equipamentos. 
 

com estes scripts você pode

  - Automatizar Rotinas de Backup em Equipamentos Mikrotik
  - Realizar rotinas de backup em lote automaticas (com a crontab)
  - Acessar os equipamentos via SSH, gerar o backup, e trazê-lo através de SCP
  - Acessar os equipamentos via FTP e trazer o arquivo de backup
  - Verificar os logs de execução das rotinas de backup

#
#
#

## como usar

quando estiver utilizando-o pela primeira vez 

    $ git clone https://github.com/M4T3U5/MikrotikB4CKUP
    $ ./MikrotikB4CKUP/install.sh
    
depois disso, você apenas pode executar (dentro da pasta do projeto)

    $ python3 main.py

onde poderá manipular o sistema ou
    
    $ python3 backup_rotine.py

para simplesmente realizar o backup


#  AJUDA

os backups e logs de execução serão gerados dentro da pasta backups, a mesma criada dentro da pasta do script.
dentro de backups, são criadas pastas com a data corrente do sistema no formato "aaaa-mm-dd", o arquivo de log 
"aaaa-mm-dd.log" e os arquivos de backup "aaaa-mm-dd_ip-equipamento_NOME-EQUIPAMENTO.txt"

obs: para que este script funcione, são necessárias as seguintes dependencias:

	- python3
	- lftp
	- openssh
	- sshpass
	- scp
	- python paramiko (biblioteca Python)

para carregar de um arquivo CSV, os atributos devem estar na seguinte ordem(aponte o caminho completo ate o arquivo):

nome(sem espaços), endereço ip(sem espaços),usuario,senha,porta,arquivo(sem espacos, com a extensão '.rsc' em equipamentos Mikrotik),protocolo('FTP' ou 'TELNET')

