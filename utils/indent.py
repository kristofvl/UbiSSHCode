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
extra = 0
for l in lines:
	numSpaces = len("".join(l)) - len("".join(l).lstrip())
	if "}" in str(l):  # do we have a block end
		n = n - 2
		extra = 0
	if "/*" in str(l):
		comment = True
	if "public:" in str(l):
		n = 1
	if "protected:" in str(l):
		n = 1
	if "private:" in str(l):
		n = 1
	if "case " in str(l):
		extra = 0	
	# don't complain about empty lines:
	lineLen = len("".join(l).strip())
	if numSpaces != (n+extra) and not comment and lineLen>0:
		line = (("".join(l)).ljust(32))[0:32].lstrip(' ')
		if n <= numSpaces:
			line = GREEN+("_"*n)+RED+("_"*(numSpaces-n))+NC+line
		else:
			line = RED+("_" * numSpaces)+NC+line
		out += BOLD+"{:03d}".format(ln)+NC+": "+line+"  "
		out += RED+" Expected "+str(n)+" spaces, found "+str(numSpaces)+NC
		out += "\n"
	# adjust expected spaces for case:
	if "case " in str(l):
		extra = "".join(l).rfind(":")+2-n
	if "{" in str(l):  # do we have a block start
		n = n + 2
	if "*/" in str(l):
		comment = False
	if "public:" in str(l):
		n = 2
	if "protected:" in str(l):
		n = 2
	if "private:" in str(l):
		n = 2
	ln = ln + 1

if 1:
	print(out)
