# UbiSSHCode
Ubiquitous SSH Code Server


Install by typing on the server:
wget https://github.com/kristofvl/UbiSSHCode/archive/refs/heads/main.zip

this command + link provides the .sh file:
wget https://github.com/kristofvl/UbiSSHCode/raw/main/webssh_project.sh

command to run the server is wsshusi

to make the server run at startup: (this method didnt work in my PC)
  1- Open Terminal
  2- Write crontab -e
  3- add the following line to it
    @reboot sh $PIPATH/webssh/startup-run.sh
   
