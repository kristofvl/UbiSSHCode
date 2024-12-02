#!/usr/bin/env python3
import sys
import csv
from subprocess import Popen, PIPE
import os
import re
from random import randrange
from pathlib import Path

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
else:
	verbose = True
subs = pth.split('/')
ename = subs[-1]  # last dir should be the exercise ID
#if verbose:
#	print("checking "+ename+" in "+str(subs))
	
if len(subs)<4 or not ename.startswith("ex"):
	print("Error: You are not in a correct exercise directory.")
	print(" (You are in " + pth + ")")
	print(ename)
	print(subs)
	exit(0)

uname = subs[2]

s = "getent passwd \""+uname+"\" | cut -d ':' -f 5"
p = Popen([s], stdout=PIPE, stderr=PIPE, shell=True, executable="/bin/bash")
stdout, stderr = p.communicate()
outstr = stdout.decode('utf-8').strip('\n').strip('\r')
if "," in outstr:
	lastn, frstn = outstr.split(',')
else:
	lastn = outstr; frstn = ""
names = outstr.strip(',').split()

# this way we form where we should be:
here = "/home/" + uname + "/" + ename

try:
	if verbose:
		out = "Checking: " + ename + "\n" 
		out += "Author:  " + frstn + " " + lastn + "\n"
		out += "User ID:  " + uname
		print(out)
	else:
		out = ename+" of "
		nm = (frstn+" "+lastn)
		out += nm.ljust(27)[:27]+", "
except NameError:
	print(RED+"Error: This directory user is not (yet) active."+NC)
	exit(0)

# open the assignments file to read which file(s) we should have:
with open('/var/local/assignments/'+ename+'.txt') as f:
	reader = csv.reader(f, delimiter = ';')
	adata = list(reader) 

# the first line has all files to check for compilation
if type(adata[0]) is not list:
	print("assignment has no target files?")
	exit(0)

# random compile file:
randfile = "/tmp/"+str(randrange(99999999))
file = ""

#with these files, check these:
for i in range(len(adata[0])):
	if verbose:
		print("opened assignment file: "+str(adata[i][0]))
	file = pth+"/"+adata[i][0]
	file_exists = os.path.isfile(file)
	if verbose:
		out = file + " "
		out += (GREEN+"exists"+NC) if file_exists else (RED+"not found."+NC)
		print(out)
	out += (GREEN+"  Y,"+NC) if file_exists else (RED+"  N,"+NC)

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
			out += GREEN+"  Y,"+NC
		else:
			if verbose:
				out = " header is "+RED+"missing "
				out += "name" if not headr_nm else ""
				out += " and " if not headr_nm and not headr_id else ""
				out += "ID" if not headr_id else ""
				out += NC
				print(out)
			out += RED+"  N,"+NC
	else: out += RED+"  N,"+NC

	# compile check:
	if file_exists:
		p = Popen(['/usr/bin/g++', '-c', file, '-o', randfile], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		if len(stderr) < 1:
			if verbose: print(" compiles "+GREEN+"fine"+NC)
			out += GREEN+"  Y,"+NC
		else:
			if verbose: print(RED+" doesn't compile"+NC)
			out += RED+"  N,"+NC
		# remove compiled file:
		p = Popen(['/usr/bin/rm', randfile], stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()
	else: out += RED+"  N,"+NC

	# cpplint check:
	if file_exists:
		p = Popen(['cpplint', file], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		stdout = str(stdout.decode('utf-8')).split("\n");
		if len(stdout) > 2:
			if verbose:
				print(" CPPLint errors: "+RED+str(stdout[1].split(": ")[-1])+NC)
				errl = str(stderr.decode('utf-8')).replace(file+":","").split("\n")
				print("  "+"\n  ".join(errl))  # TODO: remove extra \n when errors occur
			out += RED+str(stdout[1].split(": ")[-1]).rjust(4)+","+NC
		else:
			if verbose:
				print(" CPPLint errors: "+GREEN+"0"+NC)
			out += GREEN+"   0,"+NC
	else: out += RED+"   N,"+NC

	# indent check:
	if file_exists:
		p = Popen(['indent', file], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		stdout = str(stdout.decode('utf-8')).split("\n");
		if len(stdout) > 2:
			if verbose:
				print(" indent warnings: "+ORANGE+str(len(stdout)-2)+NC)
				print("  "+"\n  ".join(stdout[:-2]))
			out += ORANGE+str(len(stdout)-2).rjust(4)+","+NC
		else:
			if verbose:
				print(" indent errors: "+GREEN+"0"+NC)
			out += GREEN+"   0,"+NC
	else: out += RED+"   N,"+NC

# the last compile file is now tested:
if os.path.isfile(file):
	p = Popen(['g++', file, '-o', randfile], stdout=PIPE, stderr=PIPE, cwd=here)
	stdout, stderr = p.communicate()
	tsts = len(adata[1:])
	#with these files, check these:
	for tst in adata[1:]:
		inStr = tst[0].replace('\\\\','\\')
		inStr = re.findall(r'"([^"]*)"', tst[0])[0]
		outStr = re.findall(r'"([^"]*)"', tst[1])[0]
		try:
			p = Popen(['echo \"'+inStr+'\" | timeout 3s '+randfile+' | head -c 1k'], stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True, executable="/bin/bash")
			stdout, stderr = p.communicate()
			#print(stdout)
		# This will still result in Traceback, need to avoid this:
		except MemoryError as err:
			if verbose:
				print(" executable did not end when tested.")
		if outStr in str(stdout):
			tsts = tsts - 1
	if tsts == 0:
		out += GREEN+"   Y"+NC
		if verbose:
			print(" compiled file "+GREEN+"solves the assignment"+NC)
	else:
		out += RED+"   N"+NC
		if verbose:
			print(" compiled file "+RED+"does not fully solve assignment"+NC)
else:
	if verbose:
		print("compiled file "+RED+"not found"+NC)
	else:
		out += RED+"   N"+NC
				
# remove compiled file:
p = Popen(['/usr/bin/rm', randfile], stdout=PIPE, stderr=PIPE)
stdout, stderr = p.communicate()

# print to console:
if not verbose:
	print(out)
