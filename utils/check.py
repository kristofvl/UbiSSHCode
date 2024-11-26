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
verbose = False
if len(sys.argv) > 1:
	pth = os.path.dirname(sys.argv[1])
	if len(sys.argv)>2:
		verbose = True
subs = pth.split('/')
ename = subs[-1]  # last dir should be the exercise ID
if verbose:
	print("checking "+ename+" in "+str(subs))
	
if len(subs)!=4 or not ename.startswith("ex"):
	print("Error: You are not in a correct exercise directory.")
	print(" (You are in " + pth + ")")
	exit(0)

# read all students info:
with open('/home/kvl/list.txt', newline='') as f:
	reader = csv.reader(f)
	udata = list(reader)
if verbose:
	print("read "+str(len(udata))+" users to check against")

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
uname = ""
for i in range(len(udata)):
	if len(udata[i]) == 4:
		uname = readField( udata[i][0], "username: ")
		if uname == subs[2]:
			lastn = readField( udata[i][2], " full name:")
			frstn = readField( udata[i][3], " ")
			break
	else:
		continue
if verbose:
	print("user "+subs[2])
	if uname == subs[2]:
		print(frstn+" "+lastn+" found")
	else:
		print("not found")

# this way we form where we should be:
here = "/home/" + uname + "/" + ename

try:
	if verbose:
		out = "Checking: " + ename + "\n" 
		out += "Author:   " + frstn + " " + lastn + "\n"
		out += "User ID:  " + uname
		print(out)
	else:
		out = ename+" of "+frstn+" "+lastn+": "
except NameError:
	print(RED+"Error: This directory user is not (yet) active."+NC)
	exit(0)

# open the assignments file to read which file(s) we should have:
with open('/home/kvl/assignments/'+ename+'.txt') as f:
	reader = csv.reader(f)
	adata = list(reader)
if verbose:
	print("opened assignment file: "+str(adata))

#with these files, check these:	
for i in range(len(adata)):
	file = pth+"/"+adata[i][0]
	file_exists = os.path.isfile(file)
	if verbose:
		out = file + " "
		out += (GREEN+"exists"+NC) if file_exists else (RED+"not found.\n"+NC)
		print(out)
	out += (GREEN+"Y"+NC) if file_exists else (RED+"N"+NC)
	# header check:
	if file_exists:
		with open( file ) as f:
			code = f.read()
		headr = code.partition('/*')[2].partition('*/')[0]
		headr_nm = headr.lower().find(lastn.lower())>0
		headr_id = headr.find(uname[7:])>0
		if headr_nm and headr_id:
			if verbose:
				print(" header is "+GREEN+"fine"+NC)
			out += "\t"+GREEN+"Y"+NC
		else:
			if verbose:
				out = " header is "+RED+"missing "
				out += "name" if not headr_nm else ""
				out += " and " if not headr_nm and not headr_id else ""
				out += "ID" if not headr_id else ""
				out += NC
				print(out)
			out += "\t"+RED+"N"+NC
	else: out += "\t"+RED+"N"+NC

	# compile check:
	randfile = "/tmp/"+str(randrange(99999999))
	if file_exists:
		p = Popen(['/usr/bin/g++', '-c', file, '-o', randfile], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		if len(stderr) < 1:
			if verbose: print(" compiles "+GREEN+"fine"+NC)
			out += "\t"+GREEN+"Y"+NC
		else:
			if verbose: print(RED+"doesn't compile"+NC+",")
			out += "\t"+RED+"N"+NC
		p = Popen(['/usr/bin/rm', randfile], stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()
	else: out += "\t"+RED+"N"+NC
		
	# cpplint check:
	if file_exists:
		p = Popen(['/usr/local/bin/cpplint', file], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		stdout = str(stdout.decode('utf-8')).split("\n");
		if len(stdout) > 2:
			if verbose:
				print(" CPPLint errors: "+RED+str(stdout[1].split(": ")[-1])+NC)
			out += "\t"+RED+"N"+NC
		else:
			if verbose:
				print(" CPPLint errors: "+GREEN+"0"+NC)
			out += "\t"+GREEN+"Y"+NC
	else: out += "\t"+RED+"N"+NC

	# indent check:
	if file_exists:
		p = Popen(['/usr/bin/indent', file], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		stdout = str(stdout.decode('utf-8')).split("\n");
		if len(stdout) > 2:
			if verbose:
				print(" indent errors: "+RED+str(stdout[1].split(": ")[-1])+NC)
			out += "\t"+RED+"N"+NC
		else:
			if verbose:
				print(" indent errors: "+GREEN+"0"+NC)
			out += "\t"+GREEN+"Y"+NC
	else: out += "\t"+RED+"N"+NC
				

# print to console:
if not verbose:
	print(out)
