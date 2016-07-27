#!/usr/bin/python

import os
import re
from string import split

input = open('con_join','r')
#input = open('map_evb.gap00.dat','r')

op1 = open('map_evb.gap001', 'w')
op2 = open('map_evb.gap002', 'w')
op3 = open('map_evb.gap003', 'w')
op4 = open('map_evb.gap004', 'w')
op5 = open('map_evb.gap005', 'w')
op6 = open('map_evb.gap006', 'w')
op7 = open('map_evb.gap007', 'w')
op8 = open('map_evb.gap008', 'w')
op9 = open('map_evb.gap009', 'w')
op10 = open('map_evb.gap010', 'w')
op11 = open('map_evb.gap011', 'w')

op1.write('                   1  0.00100000 0.00    2 1.0000 0.0000   0   0.0000000   0.1000000'+'\n')
op2.write('                   1  0.00100000 0.00    2 0.9000 0.1000   0   0.1000000   0.1000000'+'\n')
op3.write('                   1  0.00100000 0.00    2 0.8000 0.2000   0   0.2000000   0.1000000'+'\n')
op4.write('                   1  0.00100000 0.00    2 0.7000 0.3000   0   0.3000000   0.1000000'+'\n')
op5.write('                   1  0.00100000 0.00    2 0.6000 0.4000   0   0.4000000   0.1000000'+'\n')
op6.write('                   1  0.00100000 0.00    2 0.5000 0.5000   0   0.5000000   0.1000000'+'\n')
op7.write('                   1  0.00100000 0.00    2 0.4000 0.6000   0   0.6000000   0.1000000'+'\n')
op8.write('                   1  0.00100000 0.00    2 0.3000 0.7000   0   0.7000000   0.1000000'+'\n')
op9.write('                   1  0.00100000 0.00    2 0.2000 0.8000   0   0.8000000   0.1000000'+'\n')
op10.write('                   1  0.00100000 0.00    2 0.1000 0.9000   0   0.9000000   0.1000000'+'\n')
op11.write('                   1  0.00100000 0.00    2 0.0000 1.0000   0   1.0000000   0.1000000'+'\n')

for line in input:
	items = split(line)
	if (int(items[0]) >= 0) and (int(items[0]) < 5000 ):
		op1.write('%d %12.3f %12.3f \n' %(int(items[0])+1, float(items[1]), float(items[2]))),
	elif (int(items[0]) >= 5000) and (int(items[0]) < 10000 ):
		op2.write('%d %12.3f %12.3f \n' %(int(items[0])-4999, float(items[1]), float(items[2]))),
        elif (int(items[0]) >= 10000) and (int(items[0]) < 15000 ):
		op3.write('%d %12.3f %12.3f \n' %(int(items[0])-9999, float(items[1]), float(items[2]))),
        elif (int(items[0]) >= 15000) and (int(items[0]) < 20000 ):
		op4.write('%d %12.3f %12.3f \n' %(int(items[0])-14999, float(items[1]), float(items[2]))),
        elif (int(items[0]) >= 20000) and (int(items[0]) < 25000 ):
		op5.write('%d %12.3f %12.3f \n' %(int(items[0])-19999, float(items[1]), float(items[2]))),
        elif (int(items[0]) >= 25000) and (int(items[0]) < 30000 ):
		op6.write('%d %12.3f %12.3f \n' %(int(items[0])-24999, float(items[1]), float(items[2]))),
        elif (int(items[0]) >= 30000) and (int(items[0]) < 35000 ):
		op7.write('%d %12.3f %12.3f \n' %(int(items[0])-29999, float(items[1]), float(items[2]))),
        elif (int(items[0]) >= 35000) and (int(items[0]) < 40000 ):
		op8.write('%d %12.3f %12.3f \n' %(int(items[0])-34999, float(items[1]), float(items[2]))),
        elif (int(items[0]) >= 40000) and (int(items[0]) < 45000 ):
		op9.write('%d %12.3f %12.3f \n' %(int(items[0])-39999, float(items[1]), float(items[2]))),
        elif (int(items[0]) >= 45000) and (int(items[0]) < 50000 ):
		op10.write('%d %12.3f %12.3f \n' %(int(items[0])-44999, float(items[1]), float(items[2]))),
        elif (int(items[0]) >= 50000) and (int(items[0]) < 55000 ):
		op11.write('%d %12.3f %12.3f \n' %(int(items[0])-49999, float(items[1]), float(items[2]))),
	
	
