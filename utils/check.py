#!/usr/bin/env python3
import sys
import csv
from subprocess import Popen, PIPE
import os
import re
from shutil import get_terminal_size
from random import randrange
#print(get_terminal_size()[0])
#from pathlib import Path

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
		#out = "\u259B"+"\u2580"*72+"\u259C"
		out = "\u250C"+"\u2500"*72+"\u2510"
		out += "\n\u2502Checking: " + ename + " "*57 + "\u2502\n" 
		out += "\u2502Author:  " + frstn + " " + lastn + " "*(62-len(frstn)-len(lastn)) + "\u2502\n"
		out += "\u2502User ID:  " + uname + " "*48 + "\u2502"
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

points = 0

#with these files, check these:
for i in range(len(adata[0])):
	if verbose:
		print("\u2502Target:   "+str(adata[0][i])+" "*(62-len(adata[0][i]))+"\u2502")
	file = pth+"/"+adata[0][i]
	file_exists = os.path.isfile(file)
	if verbose:
		out = "\u2502 " + file + " "
		out += (GREEN+"exists.   "+NC) if file_exists else (RED+"not found."+NC)
		print(out+" "*(60-len(file))+"\u2502")
	out += ("  "+GREEN+"Y"+NC+",") if file_exists else ("  "+RED+"N"+NC+",")

	# header check:
	if file_exists:
		with open( file ) as f:
			code = f.read()
		headr = code.partition('/*')[2].partition('*/')[0]
		headr_nm = headr.lower().find(lastn.lower())>0
		headr_id = headr.find(uname[7:])>0
		if headr_nm and headr_id:
			if verbose:
				print("\u2502 header is "+GREEN+"fine"+NC+" "*57+"\u2502")
			out += "  "+GREEN+"Y"+NC+","
		else:
			if verbose:
				out = "\u2502 header is "+RED+"missing "
				out += "name" if not headr_nm else ""
				out += " and " if not headr_nm and not headr_id else ""
				out += "ID" if not headr_id else ""
				out += NC
				out += " "*(84-len(out))+"\u2502"
				print(out)
			points = points - 1
			out += "  "+RED+"N"+NC+","
	else: out += "  "+RED+"N"+NC+","

	# indent check:
	if file_exists:
		p = Popen(['indent', file], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		stdout = str(stdout.decode('utf-8')).split("\n");
		if len(stdout) > 2:
			if verbose:
				errorsCnt = str(len(stdout)-2)
				print("\u2502 indent warnings: "+ORANGE+errorsCnt+NC+" "*(54-len(errorsCnt))+"\u2502")
				for lne in stdout:
					if len(lne) > 4: print("\u2502  "+lne+"    \u2502")
			points = points - 1
			out += ORANGE+str(len(stdout)-2).rjust(4)+","+NC
		else:
			if verbose:
				print("\u2502 indent warnings: "+GREEN+"0"+NC+" "*53+"\u2502")
			out += "   "+GREEN+"0"+NC+","
	else: out += "   "+RED+"N"+NC+","

	# cpplint check:
	if file_exists:
		p = Popen(['cpplint', file], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		stdout = str(stdout.decode('utf-8')).split("\n");
		if len(stdout) > 2:
			if verbose:
				errorsCnt = str(stdout[1].split(": ")[-1])
				print("\u2502 CPPLint errors: "+RED+errorsCnt+NC+" "*(55-len(errorsCnt))+"\u2502")
				errl = str(stderr.decode('utf-8')).replace(file+":","").split("\n")
				for lne in errl:
					if len(lne) > 67:
						print("\u2502  "+lne[:69]+" \u2502")
					else:
						if len(lne) > 4: print("\u2502  "+lne+" "*(69-len(lne))+" \u2502")
			points = points - 1
			out += RED+str(stdout[1].split(": ")[-1]).rjust(4)+","+NC
		else:
			if verbose:
				print("\u2502 CPPLint errors: "+GREEN+"0"+NC+" "*54+"\u2502")
			out += "   "+GREEN+"0"+NC+","
	else: out += "   "+RED+"N"+NC+","

	# compile check:
	if file_exists:
		p = Popen(['/usr/bin/g++', '-c', file, '-o', randfile], stdout=PIPE, stderr=PIPE, cwd=here)
		stdout, stderr = p.communicate()
		if len(stderr) < 1:
			if verbose: print("\u2502 compiles "+GREEN+"fine"+NC+" "*58+"\u2502")
			out += "  "+GREEN+"Y"+NC+","
		else:
			if verbose: print("\u2502"+RED+" doesn't compile"+NC+" "*58+"\u2502")
			out += "  "+RED+"N"+NC+","
		# remove compiled file:
		p = Popen(['/usr/bin/rm', randfile], stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()
	else: out += "  "+RED+"N"+NC+","

# the whole project is now tested:
if os.path.isfile(file):
	projFiles = "";
	for f in adata[0]:
		if not f.endswith(".h"):
			projFiles += " "+pth+"/"+f
	p = Popen(['g++'+projFiles+' -o'+randfile], stdout=PIPE, stderr=PIPE, shell=True,
		executable="/bin/bash")
	stdout, stderr = p.communicate()
	numTsts = len(adata[1:])
	success = 0
	#with these files, check these:
	for tst in adata[1:]:
		if "file:" in tst[0]:
			# check whether contents are in the specified file
			checkFile = pth+"/"+re.findall(r'"([^"]*)"', tst[0])[0];
			if os.path.isfile( checkFile ):
				#open file and search for string
				searchString = re.findall(r'"([^"]*)"', tst[1])[0]
				if searchString in open(checkFile).read():
					success += 1
		elif "in:" in tst[0]:
			inStr = tst[0].replace('\\\\','\\')            #
			inStr = re.findall(r'"([^"]*)"', tst[0])[0]    # get string within double quotes
			outStr = re.findall(r'"([^"]*)"', tst[1])[0]   # get string within double quotes
			andTests = True
			if len(tst)>2:
				if tst[2] == "or":
					andTests = False
			try:
				# we restrict the compiled file to be ran within 3 seconds and 1k of memory use
				p = Popen(['echo \"'+inStr+'\" | timeout 3s '+randfile+' | head -c 1k'],
					stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True, executable="/bin/bash")
				stdout, stderr = p.communicate()
				#get the output of the compiled file for analysis --- print(stdout)
			# This will still result in Traceback, need to avoid this:
			except MemoryError as err:
				if verbose:
					print("Executable did not end when tested.")
			if outStr in str(stdout).lower():
				success += 1
			else:
				if not andTests: numTsts -= 1

	if success == numTsts:
		out += "  "+GREEN+"Y"+NC
		if verbose:
			print("\u2502Assignment "+GREEN+"is solved \u263A"+NC+" "*50+"\u2502")
			#\U0001F44D\U0001F600"+NC+" "*46+"\u2502")
		points = points + 5;
	else:
		out += "  "+RED+"N"+NC
		if verbose:
			print("\u2502Assignment "+RED+"is not fully solved yet"+NC+" "*38+"\u2502")
else:
	if verbose:
		print("\u2502Compiled file "+RED+"not found"+NC+" "*49+"\u2502")
	else:
		out += "  "+RED+"N"+NC

# negative points -> zero
if points < 0: points = 0

# remove compiled file:
p = Popen(['/usr/bin/rm', randfile], stdout=PIPE, stderr=PIPE)
stdout, stderr = p.communicate()

# print to console:
if not verbose: print(out+",   "+str(points))
else: print("\u2514"+"\u2500"*72+"\u2518\n")

