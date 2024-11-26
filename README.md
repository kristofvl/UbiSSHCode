# UbiSSHCode
Ubiquitous SSH Code Server


* Install by typing on the server:
> wget https://github.com/kristofvl/UbiSSHCode/archive/refs/heads/main.zip

* this command + link provides the .sh file:
> wget https://github.com/kristofvl/UbiSSHCode/raw/main/webssh_project.sh

* execute the script: 
> bash ./webssh_project.sh 

* command to run the https server with specified cert and key file is wsshusi
   
* Daemon control

  1-to start webssh daemon type: /etc/init.d/wessh start
  
  2-to stop webssh daemon type: /etc/init.d/wessh stop
  
  3-to check the status of webssh daemon type: /etc/init.d/wessh status
  
  4-to run the script on startup type: sudo update-rc.d wessh defaults
  
  5-to stop running the script on startup type: sudo update-rc.d wessh remove

* Utilities:
  - check for inspecting a single solution
  - ex_status for inspecting all solutions for a given assignment
  - indent for checking 2-space identation
 

