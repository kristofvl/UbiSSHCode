#!/usr/bin/env python3
import sys
import csv
from subprocess import Popen, PIPE
import os
from random import randrange

RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[32;1m'
ORANGE='\033[33;1m'
BOLD='\033[0;1m'
PREVL='\033[1A'

# get exercise name:
pth = os.path.realpath(os.getcwd())
subs = pth.split('/')
if len(sys.argv) > 1:
	ename = sys.argv[1]
	verbose = True
else:
	ename = subs[-1]
	verbose = False
	
if not (ename.startswith("ex") and len(subs)==4):
	print("Error: You are not in a correct exercise directory.")
	print(" (You are in " + pth + ")")
	exit(0)

# read all students info:
with open('/home/kvl/list.txt', newline='') as f:
	reader = csv.reader(f)
	udata = list(reader)

def readField(dt, st):
	if dt.startswith( st ):
		if len(dt) > len(st):
			return dt[len(st):]
		else:
			print( "value empty, line " + str(i) )
	else:
		print( "field name missing, line " + str(i) )
	return ""

# search the current student name and ID:
for i in range(len(udata)):
	if len(udata[i]) == 4:
		uname = readField( udata[i][0], "username: ")
		if uname == subs[2]:
			lastn = readField( udata[i][2], " full name:")
			frstn = readField( udata[i][3], " ")
			break
	else:
		continue

# this way we form where we should be:
here = "/home/" + uname + "/" + ename

try:
	out = "Checking: " + ename + "\n" 
	out += "Author:   " + frstn + " " + lastn + "\n"
	out += "User ID:  " + uname + "\n"
except NameError:
	out += RED+"Error: This directory user is not (yet) active."+NC
	exit(0)

# open the assignments fiel to read which file(s) we should have:
with open('/home/kvl/assignments/'+ename+'.txt') as f:
	reader = csv.reader(f)
	adata = list(reader)

#with these files, check these:	
for i in range(len(adata)):
	file_exists = os.path.isfile( adata[i][0] )
	out += adata[i][0] + " "
	out += (GREEN+"exists"+NC) if file_exists else (RED+"not found.\n"+NC)
	vrb = (GREEN+"Y"+NC) if file_exists else (RED+"N"+NC)
	# header check:
	if file_exists:
		with open( adata[i][0] ) as f:
			code = f.read()
		headr = code.partition('/*')[2].partition('*/')[0]
		headr_nm = headr.lower().find(lastn.lower())>0
		headr_id = headr.find(uname[7:])>0
		if headr_nm and headr_id:
			out += ", header is "+GREEN+"fine"+NC
			vrb += "\t"+GREEN+"Y"+NC
		else:
			out += ", header is "+RED+"missing "
			out += "name" if not headr_nm else ""
			out += " and " if not headr_nm and not headr_id else ""
			out += "ID" if not headr_id else ""
			out += NC
			vrb += "\t"+RED+"N"+NC
	# compile check:
	randfile = "/tmp/"+str(randrange(99999999))
	if file_exists:
		p = Popen(['/usr/bin/g++', '-c', adata[i][0], '-o', randfile], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		if len(stderr) < 1:
			out += "\n  compiles "+GREEN+"fine"+NC+",\n"
			vrb += "\t"+GREEN+"Y"+NC
		else:
			out += "\n  "+RED+"doesn't compile"+NC+",\n"
			vrb += "\t"+RED+"N"+NC
		p = Popen(['/usr/bin/rm', randfile], stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()
		
	# cpplint check:
		p = Popen(['/usr/local/bin/cpplint', adata[i][0]], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		out += "  CPPLint errors: "
		stdout = str(stdout.decode('utf-8')).split("\n");
		if len(stdout) > 2:
			out += RED+str(stdout[1].split(": ")[-1])+NC
			vrb += "\t"+RED+"N"+NC
		else:
			out += GREEN+"0"+NC
			vrb += "\t"+GREEN+"Y"+NC
	# indent check:
   # indent ex000/hello.cpp -o test.cpp -d2 -brf -nbfda -nbc -npsl
		p = Popen(['/usr/bin/indent', adata[i][0], '-o', randfile,
		'-d2', '-brf', '-nbfda', '-nbc', '-npsl', '-cdw', '-br', '-ce', '-nbad', '-l120', '-npcs', '-nfca'], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		out += "\n  indentation errors: "
		errCount = 0; lCount = 0
		with open(adata[i][0]) as f1, open(randfile) as f2:
			for x, y in zip(f1, f2):
				lCount += 1
				lsx = len(x) - len(x.lstrip())
				lsy = len(y) - len(y.lstrip())
				if (lsx!=lsy):
					out += "\n   - bad indentation at "+RED+"line "
					out += str(lCount)+NC+": ["+x.strip('\n') + "]"
					errCount += 1
		if errCount < 1:
			out += GREEN+"none"+NC
			vrb += "\t"+GREEN+"Y"+NC
		else:
			vrb += "\t"+RED+"N"+NC
		out += "\n"
		p = Popen(['/usr/bin/rm', randfile], stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()

	print(vrb if verbose else out)	
   
