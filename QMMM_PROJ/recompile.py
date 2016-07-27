#!/usr/bin/python

import sys
import re
import getopt
import os.path
#import time
from string import split
from os.path import basename, splitext
from os import system
from subprocess import call
from time import clock, time

f=open('qm.log','r')
d=open('d.o','w')

line = f.readline()

forces = []
while line:
    if re.compile(' Center     Atomic                   Forces').match(line):
       line = f.readline()
       line = f.readline()
       for i in range(0,2):
         line = f.readline()
         items=split(line)
         pp = []
         for j in range(2,5):
           pp.append(float((items[j])))
         forces.append(pp)
       break
    line = f.readline()
    print line.rstrip()

for i in forces:
    x,y,z=i
    d.write('%15.10f %15.10f %15.10f\n' % (x,y,z))
#***************************************
d.close()
f.close()
