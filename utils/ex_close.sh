#!/bin/bash

# first check if user is running as root:
if [[ $EUID > 0 ]]
    then echo "please run as root"
    exit
fi

if [ $# -eq 0 ] ; then
    echo -e 'usage: sudo '$0' <year> <ex> <list.txt>'
    exit 1
fi

# for counting all errors/warnings:
ERRCOUNT=0
# arguments
ex=$2
CSV=$3

# kill all active processes of all students in <list.txt>:
while IFS=',' read -r f1 f2
do
	pkill -u ${f1:10:22}
done < "$CSV"

# copy solutions in jplag directory, read-protect dir and files:
for f in /home/st$1_*; do
	if [ -d $f ]; then
      st_dir=${f##*/}
    	if [ -d $f/$ex ]; then  # if directory exists:
        mkdir -p /home/tutor/jplag/exercises/$ex/$st_dir
        cp -r -u $f/$ex/*.cpp /home/tutor/jplag/exercises/$ex/$st_dir/
		  # change ownership of all expired exercises:
        sudo chown -R tutor:tutor /home/$st_dir/$ex/
        sudo chmod a-w /home/$st_dir/$ex/
        sudo chmod a-w /home/$st_dir/$ex/*.cpp
        sudo chmod a-w /home/$st_dir/$ex/*.h
      else  # if directory doesn't exist:
        # make an unchangeable directory to prevent starting new solutions after deadline
        sudo mkdir /home/$st_dir/$ex/
        sudo chmod a-w /home/$st_dir/$ex/
      fi
	fi
done
