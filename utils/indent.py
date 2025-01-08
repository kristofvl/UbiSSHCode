#!/usr/bin/env python3
import sys
import csv
import os

RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[32;1m'
ORANGE='\033[33;1m'
BOLD='\033[0;1m'
PREVL='\033[1A'

# get file name:
if len(sys.argv) > 1:
	try:
		fname = sys.argv[1]
		# read file, line by line:
		with open(fname, newline='') as f:
			reader = csv.reader(f, quotechar=None)
			lines = list(reader)
	except:
		print("File not found")
		exit(0)
else:
	print("Supply a file name")
	exit(0)

out = ""
n = 0  # expected spaces
ln = 1
comment = False
commentline = False
goback = False
inSwitch = False
extra = 0
for l in lines:
	ll = "".join(l)
	numSpaces = len(ll) - len(ll.lstrip())
	if ll.lstrip().startswith("//"):
		commentline = True
	# now strip away the comments to avoid detecting keywords there:
	commentIndx = ll.find("//")
	if commentIndx != -1: ll = ll[:ll.find("//")]
	# multi-line comments should not be checked:
	if "/*" in ll:
		comment = True
	# do we have a block end?
	if "}" in ll:
		if "{" in ll:
			if ll.index('{') > ll.index('}'):
				n = n- 2
				extra = 0
		else:
			n = n - 2
			extra = 0
			inSwitch = False
	if any(x in ll for x in ["private:", "protected:", "public:"]):
		n = 1
	if "case " in ll or "default" in ll:
		if not comment and not commentline:
			extra = 0
			inSwitch = True
	# don't complain about empty lines:
	lineLen = len(ll.lstrip())
	# if not the exact same nuber of spaces to n+extra, we have an error:
	if numSpaces != (n+extra) and not comment and lineLen > 0 and not commentline:
		if numSpaces == (n+2):  # after a case we can also allow a 2-space indent
			break
		line = (ll.ljust(32))[0:32].lstrip(' ')
		if n <= numSpaces:
			line = GREEN+("_"*n)+RED+("_"*(numSpaces-n))+NC+line
		else:
			line = RED+("_" * numSpaces)+NC+line
		out += BOLD+"{:03d}".format(ln)+NC+": "+line+"  "
		out += RED+" Expected "+str(n+extra)+" spaces, found "+str(numSpaces)+NC
		out += "\n"
	# adjust expected spaces for case:
	if "case " in ll and not "break" in ll:
		if not comment and not commentline:
			extra = ll.rfind(":")+2-n
	if "default " in ll and not "break" in ll:
		if not comment and not commentline:
			extra = ll.rfind(":")+2-n
	# for if statements without {}
	if goback:
		n = n - 2
		goback = False
	if "if" in ll and not "{" in ll and not ";" in ll and not comment and not commentline:
		n = n + 2
		goback = True
	if "else" in ll and not "{" in ll and not ";" in ll:
		n = n + 2
		goback = True
	if "{" in ll:  # do we have a block start
		if "}" in ll:
			if ll.index('{') > ll.index('}'):
				n = n + 2
		else:
			n = n + 2
	if "*/" in ll:
		comment = False
	if any(x in ll for x in ["private:", "protected:", "public:"]):
		n = 2
	ln = ln + 1
	commentline = False
if 1:
	print(out)
