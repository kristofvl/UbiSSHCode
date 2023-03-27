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
echo current 4-digit-year command is set to MYDATE
echo -e "\e[37m"
echo -e "\e[36m \e[5mDOWNLOADING PACKAGES \e[25m\e[37m"
wget https://github.com/huashengdun/webssh/archive/refs/heads/master.zip
unzip master.zip
rm master.zip
echo -e "\e[37m"
echo -e "\e[36m \e[5mINSTALLING PACKAGES \e[25m\e[37m"
echo -e "\e[32m INSTALL WEBSSH \e[37m"
pip install webssh
rm -r webssh-master
echo -e "\e[32m Done! \e[37m"
echo -e "\e[32m LOCATING INSTALLATION PATH \e[37m"
python3 -m pip show webssh > installation-path.sh
sudo sed -i '1,7d;9d;$d' installation-path.sh
echo -e "\e[32m Done! \e[37m"
echo -e "\e[32m MAKING AN ENVIRONMENT PATH \e[37m"
sudo sed -i 's/Location: /export PIPATH=/g' installation-path.sh
sudo chmod a+x installation-path.sh
source installation-path.sh
rm installation-path.sh
cd $PIPATH/webssh/templates
echo -e "\e[32m Done! \e[37m"
echo -e "\e[37m"
echo -e "\e[36m \e[5mREMOVE CURRENT HTML FILE \e[25m\e[37m"
rm index.html
echo "index.html has been removed"
echo -e "\e[36m \e[5mCREATE NEW HTML FILE \e[25m"
echo -e "\e[37m"
touch index.html
echo "file created"
echo -e "\e[36m \e[5mWRITING TO FILE \e[25m"
echo -e "\e[37m"
echo "<""!""DOCTYPE html>" >> index.html
echo "<html lang=\"en\">" >> index.html
echo   "<head>" >> index.html
echo     "<meta charset=\"UTF-8\">" >> index.html
echo     "<title> WebSSH </title>" >> index.html
echo     "<link href=\"static/img/favicon.png\" rel=\"icon\" type=\"image/png\">" >> index.html
echo     "<link href=\"static/css/bootstrap.min.css\" rel=\"stylesheet\" type=\"text/css\"/>" >> index.html
echo     "<link href=\"static/css/xterm.min.css\" rel=\"stylesheet\" type=\"text/css\"/>" >> index.html
echo     "<link href=\"static/css/fullscreen.min.css\" rel=\"stylesheet\" type=\"text/css\"/>" >> index.html
echo     "<style>" >> index.html
echo       ".row {" >> index.html
echo         "margin-top: 15px;" >> index.html
echo         "margin-bottom: 10px;" >> index.html
echo       "}" >> index.html
echo       ".container {" >> index.html
echo         "margin-top: 20px;" >> index.html
echo       "}" >> index.html
echo       ".btn {" >> index.html
echo         "margin-top: 15px;" >> index.html
echo       "}" >> index.html
echo       ".btn-danger {" >> index.html
echo         "margin-left: 5px;" >> index.html
echo       "}" >> index.html
echo       "{% if font.family %}" >> index.html
echo       "@font-face {" >> index.html
echo         "font-family: '{{ font.family }}';" >> index.html
echo         "src: url('{{ font.url }}');" >> index.html
echo       "}" >> index.html
echo       "body {" >> index.html
echo         "font-family: '{{ font.family }}';" >> index.html
echo       "}" >> index.html
echo       "{% end %}" >> index.html
echo     "</style>" >> index.html
echo   "</head>" >> index.html
echo   "<body>" >> index.html
echo     "<div id=\"waiter\" style=\"display: none\"> Connecting ... </div>" >> index.html
echo     "<div class=\"container form-container\" style=\"display: none\">" >> index.html
echo       "<form id=\"connect\" action=\"\" method=\"post\" enctype=\"multipart/form-data\"{% if debug %} novalidate{% end %}>" >> index.html
echo         "<div class=\"row\">" >> index.html
echo           "<div class=\"col\">" >> index.html
echo             "<label for=\"Hostname\">Hostname</label>" >> index.html
echo             "<input class=\"form-control\" type=\"text\" id=\"hostname\" name=\"hostname\" placeholder=\"$HOSTNAME\" value=\"$HOSTNAME\" readonly>" >> index.html
echo           "</div>" >> index.html
echo         "</div>" >> index.html
echo         "<div class=\"row\">" >> index.html
echo           "<div class=\"col\">" >> index.html
echo             "<label for=\"Username\">Username</label>" >> index.html
echo             "<input class=\"form-control\" type=\"text\" id=\"username\" name=\"username\" placeholder=\"st$MYDATE\"value=\"st$MYDATE\" required>" >> index.html
echo           "</div>" >> index.html
echo           "<div class=\"col\">" >> index.html
echo             "<label for=\"Password\">Password</label>" >> index.html
echo             "<input class=\"form-control\" type=\"password\" id=\"password\" name=\"password\" value=\"\">" >> index.html
echo           "</div>" >> index.html
echo         "</div>" >> index.html
echo         "<input type=\"hidden\" id=\"term\" name=\"term\" value=\"xterm-256color\">" >> index.html
echo         "{% module xsrf_form_html() %}" >> index.html
echo         "<button type=\"submit\" class=\"btn btn-primary\">Connect</button>" >> index.html
echo         "<button type=\"reset\" class=\"btn btn-danger\">Reset</button>" >> index.html
echo       "</form>" >> index.html
echo     "</div>" >> index.html
echo     "<div class=\"container\">" >> index.html
echo       "<div id=\"status\" style=\"color: red;\"></div>" >> index.html
echo       "<div id=\"terminal\"></div>" >> index.html
echo     "</div>" >> index.html
echo     "<script src=\"static/js/jquery.min.js\"></script>" >> index.html
echo     "<script src=\"static/js/popper.min.js\"></script>" >> index.html
echo     "<script src=\"static/js/bootstrap.min.js\"></script>" >> index.html
echo     "<script src=\"static/js/xterm.min.js\"></script>" >> index.html
echo     "<script src=\"static/js/xterm-addon-fit.min.js\"></script>" >> index.html
echo     "<script src=\"static/js/main.js\"></script>" >> index.html
echo   "</body>" >> index.html
echo "</html>" >> index.html
