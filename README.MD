# MIKROTIK B4CKUP
#
#
#
 ### Mikrotik Systems backup is an simple code which runs some scripts to do backup rotines into Mikrotik equipaments.

with this script you can do

  - Batch Backup Rotines   
  - Automated Backup Routines (with crontab)
  - Get backup configuration by SSH or FTP
#
#
#

## how to use it

when you running project for first time 

    $ git clone https://github.com/M4T3U5/MikrotikB4CKUP
    $ ./MikrotikB4CKUP/get_dependences.sh
    
after that, you just can call

    $ python3 main.py
where you can manage your devices and backups or just
    
    $ python3 backup_rotine.py
to do the backups ;)
