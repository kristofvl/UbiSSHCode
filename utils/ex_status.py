#!/usr/bin/env python3
import sys
import csv
from subprocess import Popen, PIPE
import os

if len(sys.argv) < 2:
	print("please provide an exercise")
	exit(0)
else:
	ename = sys.argv[1]

with open('list.txt', newline='') as f:
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

	out = "directory missing\t\t"
	if os.path.isdir(expth):
		#p = Popen(["/home/kvl/check.py", ename], cwd=expth, stdout=PIPE, stderr=PIPE)
		p = Popen(["check", ename], cwd=expth, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()
		out = stdout.decode("utf-8")
		y = out.count('Y')
		n = out.count('N')
		if y > 4 and n == 0:
			countP += 1
		ans = out.split('\t');
		if len(ans)>1:
			if ans[2].count('Y') > 0: # compiles?
				countC += 1
			#if ans[3].count('Y') > 0: # works?		
			#	countW += 1
	else:
		countM += 1

	print(uname + ":\t" + out.rstrip('\n') + "\t"+lastn)


print(str(countM) + " students have no solution" )
print(str(countC) + " students have a compiling solution" )
#print(str(countW) + " students have a working solution" )
print(str(countP) + " students have a perfect solution" )
