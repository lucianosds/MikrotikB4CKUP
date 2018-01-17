##############
clear

echo " \n ATUALIZANDO LISTA DE REPOSITORIOS \n"
apt update

echo "\n INSTALANDO DEPENDENCIAS \n"
apt install openssh
apt install lftp
apt install sshpass
apt install python3
apt install python3-pip
apt install pip3
python3-pip install paramiko
pip3 install paramiko
clear
python3 main.py
##############
