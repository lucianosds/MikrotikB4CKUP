##############
clear

echo " \n ATUALIZANDO LISTA DE REPOSITORIOS \n"
apt update

echo "\n INSTALANDO DEPENDENCIAS 1/6 \n"
apt install openssh
echo "\n INSTALANDO DEPENDENCIAS 2/6 \n"
apt install lftp
echo "\n INSTALANDO DEPENDENCIAS 3/6 \n"
apt install sshpass
echo "\n INSTALANDO DEPENDENCIAS 4/6 \n"
apt install python3
echo "\n INSTALANDO DEPENDENCIAS 5/6 \n"
apt install python3-pip
echo "\n INSTALANDO DEPENDENCIAS 6/6 \n"
pip3 install paramiko

clear
python3 main.py
##############
