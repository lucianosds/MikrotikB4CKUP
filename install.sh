##############
clear

echo "  ATUALIZANDO LISTA DE REPOSITORIOS "
echo 
sudo apt update
echo
echo " INSTALANDO DEPENDENCIAS 1/6 "
echo
sudo apt install openssh
echo
echo " INSTALANDO DEPENDENCIAS 2/6 "
echo
sudo apt install lftp
echo
echo " INSTALANDO DEPENDENCIAS 3/6 "
echo
sudo apt install sshpass
echo
echo " INSTALANDO DEPENDENCIAS 4/6 "
echo
sudo apt install python3
echo
echo " INSTALANDO DEPENDENCIAS 5/6 "
echo
sudo apt install python3-pip
echo
echo " INSTALANDO DEPENDENCIAS 6/6 "
echo
pip3 install paramiko

clear
python3 main.py
##############
