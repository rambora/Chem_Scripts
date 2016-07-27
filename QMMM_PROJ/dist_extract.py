#!/opt/python/bin/python

import os
import re
from string import split
import numpy as np
'''
for i in range(15,37, 2):

	input = open('./is_pmf_'+str(i)+'/dist.dat', 'r')
	output = open('pmf_'+str(i)+'_1.dat','w')


	output.write('# DROFF =%15.8f K =   200.00000000 \n' % (i/10.0))
	for line in input:
		if '         1         3' in line:
			items = split(line)
			output.write(items[3] + '\n')
	output.close()
'''

os.rename("pmf_15_1.dat", "pmf_1_1.dat")
os.rename("pmf_17_1.dat", "pmf_2_1.dat")
os.rename("pmf_19_1.dat", "pmf_3_1.dat")
os.rename("pmf_21_1.dat", "pmf_4_1.dat")
os.rename("pmf_23_1.dat", "pmf_5_1.dat")
os.rename("pmf_25_1.dat", "pmf_6_1.dat")
os.rename("pmf_27_1.dat", "pmf_7_1.dat")
os.rename("pmf_29_1.dat", "pmf_8_1.dat")
os.rename("pmf_31_1.dat", "pmf_9_1.dat")
os.rename("pmf_33_1.dat", "pmf_10_1.dat")
os.rename("pmf_35_1.dat", "pmf_11_1.dat")

#input.close()


