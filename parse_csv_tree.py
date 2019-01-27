#!/usr/bin/env python

import sys

if len(sys.argv[1:]) < 2:
	sys.stderr.write("ERROR: missing argument\nUsage:\nparse_csv_tree.py <tree.csv> <tree.new.csv>\n\n")
	sys.exit(1)


it,ot = sys.argv[1:]

f = open(it,'r')
f = f.readlines()
o = open(ot,'w')

dic_h = {}
c = 0
for branch in f:
	branch = branch.split(',')
	dic_h[c]=''
	for x in xrange(len(branch)):
		if branch[x] == '':
			pass
		else:
			if branch[x] != "NoLabel" and branch[x][0].isupper():
				dic_h[c] = (x,branch[x])
				print dic_h[c],c,branch
				new_line = map(lambda x:str(x),branch)
				new_line = ','.join(new_line).strip()
				o.write(new_line+'\n')
				break
			elif branch[x] == "NoLabel":
				print 'Here is the problem',c,x
				z = c-1
				while z > 0:
					print dic_h[z],z,branch[x],x
					if dic_h[z][0] < x:
						distance = str(c-z)
						print "distance",distance
						new_label = dic_h[z][1]+"_"+str(branch[x+1]).strip()
						dic_h[c] = (x,new_label)
						branch[x] = new_label
						new_line = map(lambda x:str(x),branch)
						new_line = ','.join(new_line).strip()
						break
						o.write(new_line+'\n')
					else:
						z = z-1

			else:
				pass
	c += 1
o.close()
