echo -e "\e[37m"
echo -e "\e[36m \e[5mUPDATE SYSTEM \e[25m\e[37m"
sudo apt-get update
echo -e "\e[37m"
echo -e "\e[36m \e[5mINSTALLING NECESSARY COMMANDS \e[25m\e[37m"
echo -e "\e[32m PIP COMMAND \e[37m"
sudo apt install python3-pip
echo -e "\e[32m WGET COMMAND \e[37m"
sudo apt install wget
echo -e "\e[32m UNZIP COMMAND \e[37m"
sudo apt install unzip
echo -e "\e[32m SED COMMAND \e[37m"
sudo apt install sed
echo -e "\e[32m SOURCE COMMAND \e[37m"
sudo apt install source
echo -e "\e[37m"
echo -e "\e[36m \e[5mINSTALLING SHELL VARIABLES \e[25m\e[37m"
MYDATE=$(date +%Y)_
echo "current 4-digit-year command is set to MYDATE"
echo -e "\e[37m"
echo -e "\e[36m \e[5mDOWNLOADING PACKAGES \e[25m\e[37m"
sudo wget https://github.com/huashengdun/webssh/archive/refs/heads/master.zip
sudo unzip master.zip
sudo rm -r master.zip
echo -e "\e[37m"
echo -e "\e[36m \e[5mINSTALLING PACKAGES \e[25m\e[37m"
echo -e "\e[32m INSTALL WEBSSH \e[37m"
sudo pip install webssh
sudo rm -r webssh-master
echo -e "\e[32m Done! \e[37m"
echo -e "\e[32m LOCATING INSTALLATION PATH \e[37m"
sudo python3 -m pip show webssh > installation-path.sh
sudo sed -i '1,7d;9d;$d' installation-path.sh
echo -e "\e[32m Done! \e[37m"
echo -e "\e[32m MAKING AN ENVIRONMENT PATH \e[37m"
sudo sed -i 's/Location: /export PIPATH=/g' installation-path.sh
sudo chmod a+x installation-path.sh
source installation-path.sh
sudo ./installation-path.sh
sudo rm installation-path.sh
cd $PIPATH/webssh/templates
echo -e "\e[32m Done! \e[37m"
echo -e "\e[37m"
echo -e "\e[36m \e[5mREMOVE CURRENT HTML FILE \e[25m\e[37m"
sudo rm index.html
echo "index.html has been removed"
echo -e "\e[36m \e[5mCREATE NEW HTML FILE \e[25m"
echo -e "\e[37m"
sudo touch index.html
echo "file created"
echo -e "\e[36m \e[5mWRITING TO FILE \e[25m"
echo -e "\e[37m"
sudo echo "<""!""DOCTYPE html>" | sudo tee -a index.html
sudo echo "<html lang=\"en\">" | sudo tee -a index.html
sudo echo   "<head>" | sudo tee -a index.html
sudo echo     "<meta charset=\"UTF-8\">" | sudo tee -a index.html
sudo echo     "<title> WebSSH </title>" | sudo tee -a index.html
sudo echo     "<link href=\"static/img/favicon.png\" rel=\"icon\" type=\"image/png\">" | sudo tee -a index.html
sudo echo     "<link href=\"static/css/bootstrap.min.css\" rel=\"stylesheet\" type=\"text/css\"/>" | sudo tee -a index.html
sudo echo     "<link href=\"static/css/xterm.min.css\" rel=\"stylesheet\" type=\"text/css\"/>" | sudo tee -a index.html
sudo echo     "<link href=\"static/css/fullscreen.min.css\" rel=\"stylesheet\" type=\"text/css\"/>" | sudo tee -a index.html
sudo echo     "<style>" | sudo tee -a index.html
sudo echo       ".row {" | sudo tee -a index.html
sudo echo         "margin-top: 15px;" | sudo tee -a index.html
sudo echo         "margin-bottom: 10px;" | sudo tee -a index.html
sudo echo       "}" | sudo tee -a index.html
sudo echo       ".container {" | sudo tee -a index.html
sudo echo         "margin-top: 20px;" | sudo tee -a index.html
sudo echo       "}" | sudo tee -a index.html
sudo echo       ".btn {" | sudo tee -a index.html
sudo echo         "margin-top: 15px;" | sudo tee -a index.html
sudo echo       "}" | sudo tee -a index.html
sudo echo       ".btn-danger {" | sudo tee -a index.html
sudo echo         "margin-left: 5px;" | sudo tee -a index.html
sudo echo       "}" | sudo tee -a index.html
sudo echo       "{% if font.family %}" | sudo tee -a index.html
sudo echo       "@font-face {" | sudo tee -a index.html
sudo echo         "font-family: '{{ font.family }}';" | sudo tee -a index.html
sudo echo         "src: url('{{ font.url }}');" | sudo tee -a index.html
sudo echo       "}" | sudo tee -a index.html
sudo echo       "body {" | sudo tee -a index.html
sudo echo         "font-family: '{{ font.family }}';" | sudo tee -a index.html
sudo echo       "}" | sudo tee -a index.html
sudo echo       "{% end %}" | sudo tee -a index.html
sudo echo     "</style>" | sudo tee -a index.html
sudo echo   "</head>" | sudo tee -a index.html
sudo echo   "<body>" | sudo tee -a index.html
sudo echo     "<div id=\"waiter\" style=\"display: none\"> Connecting ... </div>" | sudo tee -a index.html
sudo echo     "<div class=\"container form-container\" style=\"display: none\">" | sudo tee -a index.html
sudo echo       "<form id=\"connect\" action=\"\" method=\"post\" enctype=\"multipart/form-data\"{% if debug %} novalidate{% end %}>" | sudo tee -a index.html
sudo echo         "<div class=\"row\">" | sudo tee -a index.html
sudo echo           "<div class=\"col\">" | sudo tee -a index.html
sudo echo             "<label for=\"Hostname\">Hostname</label>" | sudo tee -a index.html
sudo echo             "<input class=\"form-control\" type=\"text\" id=\"hostname\" name=\"hostname\" placeholder=\"$HOSTNAME\" value=\"$HOSTNAME\" readonly>" | sudo tee -a index.html
sudo echo           "</div>" | sudo tee -a index.html
sudo echo         "</div>" | sudo tee -a index.html
sudo echo         "<div class=\"row\">" | sudo tee -a index.html
sudo echo           "<div class=\"col\">" | sudo tee -a index.html
sudo echo             "<label for=\"Username\">Username</label>" | sudo tee -a index.html
sudo echo             "<input class=\"form-control\" type=\"text\" id=\"username\" name=\"username\" placeholder=\"st$MYDATE\"value=\"st$MYDATE\" required>" | sudo tee -a index.html
sudo echo           "</div>" | sudo tee -a index.html
sudo echo           "<div class=\"col\">" | sudo tee -a index.html
sudo echo             "<label for=\"Password\">Password</label>" | sudo tee -a index.html
sudo echo             "<input class=\"form-control\" type=\"password\" id=\"password\" name=\"password\" value=\"\">" | sudo tee -a index.html
sudo echo           "</div>" | sudo tee -a index.html
sudo echo         "</div>" | sudo tee -a index.html
sudo echo         "<input type=\"hidden\" id=\"term\" name=\"term\" value=\"xterm-256color\">" | sudo tee -a index.html
sudo echo         "{% module xsrf_form_html() %}" | sudo tee -a index.html
sudo echo         "<button type=\"submit\" class=\"btn btn-primary\">Connect</button>" | sudo tee -a index.html
sudo echo         "<button type=\"reset\" class=\"btn btn-danger\">Reset</button>" | sudo tee -a index.html
sudo echo       "</form>" | sudo tee -a index.html
sudo echo     "</div>" | sudo tee -a index.html
sudo echo     "<div class=\"container\">" | sudo tee -a index.html
sudo echo       "<div id=\"status\" style=\"color: red;\"></div>" | sudo tee -a index.html
sudo echo       "<div id=\"terminal\"></div>" | sudo tee -a index.html
sudo echo     "</div>" | sudo tee -a index.html
sudo echo     "<script src=\"static/js/jquery.min.js\"></script>" | sudo tee -a index.html
sudo echo     "<script src=\"static/js/popper.min.js\"></script>" | sudo tee -a index.html
sudo echo     "<script src=\"static/js/bootstrap.min.js\"></script>" | sudo tee -a index.html
sudo echo     "<script src=\"static/js/xterm.min.js\"></script>" | sudo tee -a index.html
sudo echo     "<script src=\"static/js/xterm-addon-fit.min.js\"></script>" | sudo tee -a index.html
sudo echo     "<script src=\"static/js/main.js\"></script>" | sudo tee -a index.html
sudo echo   "</body>" | sudo tee -a index.html
sudo echo "</html>" | sudo tee -a index.html

echo -e "\e[37m"
echo -e "\e[36m \e[5mCreating an Alias Command (wsshusi) for our wssh key and cert file \e[25m\e[37m"
alias wsshusi='sudo wssh --certfile=/etc/letsencrypt/live/ubi21.informatik.uni-siegen.de/cert.pem --keyfile=/etc/letsencrypt/live/ubi21.informatik.uni-siegen.de/privkey.pem --sslport=8888 --port=4433'
echo "Specific Command to run Uni-Siegen Web SSH Server is: wsshusi"
echo -e "\e[37m"
echo -e "\e[36m \e[5mMaking startup file \e[25m\e[37m"
cd /etc/init.d/
echo "path changed to /etc/init.d/"
sudo touch startup-run.sh
echo "startup-run.sh file created"
echo "writing to startup-run.sh file"







sudo echo "sudo wssh --certfile=/etc/letsencrypt/live/ubi21.informatik.uni-siegen.de/cert.pem --keyfile=/etc/letsencrypt/live/ubi21.informatik.uni-siegen.de/privkey.pem --sslport=8888 --port=4433" | sudo tee startup-run.sh
echo "done!"
echo "Making file executable:"
sudo chmod a+x startup-run.sh
