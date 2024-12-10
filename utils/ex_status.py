#!/usr/bin/env python3
import sys
import csv
from subprocess import Popen, PIPE
import os
from pathlib import Path

if len(sys.argv) < 2:
	print("please provide an exercise")
	exit(0)
else:
	ename = sys.argv[1]

verbose = True
if len(sys.argv) > 2:
	if sys.argv[2] == "v":
		verbose = False;

with open(str(Path.home())+"/list.txt", newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

def readField(dt, st):
	if dt.startswith( st ):
		if len(dt) > len(st):
			return dt[len(st):]
		else:
			print( "value empty, line " + str(i) )
	else:
		print( "field name missing, line " + str(i) )
	return ""

countM = 0 # missing solutions
countP = 0 # perfect solutions
countW = 0 # working solutions
countC = 0 # compiling solutions

# open moodle csv file for marking:
if len(sys.argv) > 2:
	r = csv.reader( open(sys.argv[2]) )
	lines = list(r)
	print(lines[1][0]+lines[1][1])

for i in range(len(data)):
	if len(data[i]) == 4:
		uname = readField( data[i][0], "username: ")
		passw = readField( data[i][1], " password: ")
		lastn = readField( data[i][2], " full name:")
		frstn = readField( data[i][3], " ")
	else:
		print("error in reading line" + i)
		continue

	expth = "/home/"+uname+"/"+ename

	if not verbose:
		with open(str(Path.home())+"/assignments/"+ename+".txt") as f:
			fname = f.readline().strip('\n')
		#print(fname)
		p = Popen(['source-highlight','-n','--infer-lang','-f','esc','--style-file=esc.style','-i',expth+'/'+fname])
		#source-highlight -n --infer-lang -f esc --style-file=esc.style -i $f
		input("\nPress Enter to continue\n")
		continue

	score = '-'
	p = Popen([str(Path.home())+"/UbiSSHCode/utils/check.py", expth+"/"+ename], stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	out = stdout.decode("utf-8")
	print(uname + " " + out[9:].rstrip('\n'))
	out = out[9+28:].strip('\n').split(',')
	if out[0].count('N') > 0:
		countM += 1
	if len(out) > 5:
		if out[5].count('Y') > 0:
			countW += 1
	if len(out) > 4:
		if out[4].count('Y') > 0:
			countC += 1
	if len(out) > 6:
		score = float(out[6].lstrip(' '))
		if score ==5:
			countP += 1

	#find student in csv:
	if len(sys.argv) > 2:
		personFound = False
		for row in lines:
			if row[0]==frstn and row[1]==lastn:
				personFound = True
				row[9]="{:.2f}".format(score)
		if not personFound:
			print("?")

print(str(countM) + " students have no solution" )
print(str(countC) + " students have a compiling solution" )
print(str(countW) + " students have a working solution" )
print(str(countP) + " students have a perfect solution" )

with open('intro.csv', 'w', newline='', encoding='utf-8') as f:
	w = csv.writer(f)
	w.writerows(lines)
