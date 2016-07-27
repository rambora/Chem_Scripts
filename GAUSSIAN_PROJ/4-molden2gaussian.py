#!/usr/bin/python


# same as " 3-molden2gaussian.py "  with the only difference that here all the subportions are read/imported 
import os

def main():

 input = 'molden.xyz'
# output = 'gaussian4.com'

 inp=open(input,'r')
 out1=open('gau1.com','w')

 lines=inp.readlines()
 out1.writelines(lines[2:])

 inp.close()
 out1.close()


if __name__ == "__main__":
   main()

#-------------------------------------------

import gaussian_sub                      # making the substitutions "C" with "C  0" etc
import gaussian_header                   # adding the gaussian header and pasting the coords
import gaussian_tail                     # appending the tail
import gaussian_meta_remove              # removing all the intermediate meta files

#--------------------------------------------

#if __name__ == "__main__":
#   main()

exit()



