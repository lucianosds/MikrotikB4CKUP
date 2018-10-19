##############
clear

# Updating repository list
echo "  ATUALIZANDO LISTA DE REPOSITORIOS "
echo 
sudo apt update
echo
# Installing dependencies 1/6 - openssh
echo " INSTALANDO DEPENDENCIAS 1/6 "
echo
sudo apt install openssh
echo
# Installing dependencies 2/6 - lftp
echo " INSTALANDO DEPENDENCIAS 2/6 "
echo
sudo apt install lftp
echo
# Installing dependencies 3/6 - sshpass
echo " INSTALANDO DEPENDENCIAS 3/6 "
echo
sudo apt install sshpass
echo
# Installing dependencies 4/6 - python3
echo " INSTALANDO DEPENDENCIAS 4/6 "
echo
sudo apt install python3
echo
# Installing dependencies 5/6 - python3-pip
echo " INSTALANDO DEPENDENCIAS 5/6 "
echo
sudo apt install python3-pip
echo
# Installing dependencies 6/6 - paramiko
echo " INSTALANDO DEPENDENCIAS 6/6 "
echo
pip3 install paramiko

clear
python3 main.py
##############
