#!/usr/bin/python


# This program converts the molden output files into gaussian compatible input files
# "input" and "output" file names are needed to change accordingly
# The intermediate meta file created "gau1.com" will be removed at the end of the run

import os

input = 'molden.xyz'
output = 'gaussian.com'

inp=open(input,'r')
out1=open('gau1.com','w')


lines=inp.readlines()
out1.writelines(lines[2:])

inp.close()
out1.close()

out2=open('gau1.com','r')
out3=open(output,'w')

# writing the header text

out3.write('%chk=blact-trunc-34.chk \n')
out3.write('%mem=3GB \n')
out3.write('%nproc=16 \n')
out3.write('#p opt(modredundant) b3lyp/gen nosymm guess=read pseudo=read scf=(conver=8,maxcycles=250) int=ultrafine \n \n')
out3.write('Title Card Required \n \n')
out3.write('0 1 \n')

# adding the coordinates

for line in out2:
       out3.write(line)


out2.close()
out3.close()

# appending the text

out4=open(output,'a')

out4.write('\nB 1 2 \n \n')
out4.write('C H O N S 0 \n')
out4.write('6-31+G* \n')
out4.write('**** \n')
out4.write('Zn 0 \n')
out4.write('LANL2DZ \n')
out4.write('**** \n \n')
out4.write('Zn 0 \n')
out4.write('LANL2DZ \n \n \n \n')

out4.close()

#os.remove('gau1.com')
exit()



