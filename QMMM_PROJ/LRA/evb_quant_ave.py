#!/usr/bin/python

import re
from string import split

input = open('./rs_evb_pm6/rs_evb_pm6.out','r')
evb_output = open('evb-energy.dat', 'w')
quant_output = open('quant-energy.dat', 'w')

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

evb_ave = open('evb-energy.dat','r').readlines()
N = len(evb_ave)
print "Total points:", N
sum1 = 0.0
for i in evb_ave:
    sum1 = sum1 + float(i)

print "evb_ave:= ", sum1/N
print
print

quant_ave = open('quant-energy.dat','r').readlines()
N = len(quant_ave)
print "Total points:", N
sum2 = 0.0
for i in quant_ave:
    sum2 = sum2 + float(i)

print "quant_ave:= ", sum2/N
print

evb_ene_diff = (sum2/N) - (sum1/N)

print "(<E2-E1>)evb =", evb_ene_diff
#evb_ave.close()
#quant_ave.close()

