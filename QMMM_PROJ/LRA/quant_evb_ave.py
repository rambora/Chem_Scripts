#!/usr/bin/python

import re
from string import split

input = open('./QM-TRAJ/rs_pm6_evb/rs_pm6_evb.out','r')
evb_output = open('qtr-evb-energy.dat', 'w')
quant_output = open('qtr-quant-energy.dat', 'w')

for line in input.readlines():

     if 'E_evb(eminus)=' in line:
        items = split(line)
        evb_output.write(items[1] + '\n')

     else:

        if ' Equantum =     ' in line:
           items = split(line)
           quant_output.write(items[2] + '\n')

evb_output.close()
quant_output.close()       
input.close()

print
print

evb_ave = open('qtr-evb-energy.dat','r').readlines()
N = len(evb_ave)
print "Total points:", N
sum1 = 0.0
for i in evb_ave:
    sum1 = sum1 + float(i)

print "qtr-evb_ave:= ", sum1/N
print
print

quant_ave = open('qtr-quant-energy.dat','r').readlines()
N = len(quant_ave)
print "Total points:", N
sum2 = 0.0
for i in quant_ave:
    sum2 = sum2 + float(i)

print "qtr-quant_ave:= ", sum2/N
print

quant_ene_diff = (sum1/N) - (sum2/N)

print "(<E2-E1>)quant =", quant_ene_diff
#evb_ave.close()
#quant_ave.close()

