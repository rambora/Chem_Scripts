#!/usr/bin/python

import sys
import os

def main():

 filename = '3FCZ'   # write the name of the pdb file without ".pdb" extension

 input = filename+".pdb"
 output = filename+"_mod.pdb"

 output1 = filename+"-1.pdb"

 inp=open(input, 'r')
 out1=open(output1, 'w')

 for line in inp.readlines():
  split = line.split()
  if split[0] == 'ATOM' or split[0] == 'HETATM':
     if split[4] == 'A':
        out1.write(line[:-25] + "\n")

 out1.close()

 inp3=open('3FCZ-1.pdb', 'r')
 out3 = open(output,'w')
 inp4=inp3.read()
 out4 = inp4.replace("HETATM" , "ATOM  ")
 out3.write(out4)


if __name__ == "__main__":
   main()   

#os.remove(output1)

exit()
