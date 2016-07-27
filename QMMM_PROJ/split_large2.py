#!/usr/bin/python

import os
import sys
from string import split
import pandas as pd

try:
	os.remove('con_join')
	for i in range(1,12):
                os.remove('test_'+str(i))
except OSError:
	pass

df1 = pd.read_csv('rs_qm1_pm3.dat', header=None)
df2 = pd.read_csv('rs_qm2_pm6.dat', header=None)

con_join = pd.concat([df1,df2],axis=1) # pasting kind -- next to each other

#con_join = pd.concat([df1,df2], axis=0)   # regular concatenation -- join kind

df_out = con_join.to_csv('con_join',header=None, sep='\t')



input = open('con_join','r')

k = 5000
for line in input:
	items = split(line)
	for i in range(0,12):
		j = i+1
		if (int(items[0]) >= i*k) and (int(items[0]) < j*k ):
			out = open('test_'+str(j),'a')
#			out.write('                   1  0.00100000 0.00    2 1.0000 0.0000   0   0.0000000   0.1000000')
			out.write('%d %12.3f %12.3f \n' %(int(items[0])-((i*k)-1), float(items[1]), float(items[2])))


