#!/usr/bin/python


# This program converts the molden output files into gaussian compatible input files
# "input" and "output" file names are needed to change accordingly
# The intermediate meta file created "gau1.com" will be removed at the end of the run

import os

input = 'molden.xyz'
output = 'gaussian2.com'

inp=open(input,'r')
out1=open('gau1.com','w')


lines=inp.readlines()
out1.writelines(lines[2:])

inp.close()
out1.close()

#***********************************
out2=open('gau1.com','r')
out3=open(output,'w')

#----------------------------------
oc=open('out-c.xyz','w')
oh=open('out-h.xyz','w')
on=open('out-n.xyz','w')
oo=open('out-o.xyz','w')
os=open('out-s.xyz','w')
oz=open('out-z.xyz','w')

s = out2.read()

z1 = s.replace("C", "C   0")
oc.write(z1)
oc.close()
#**********************
oc2=open('out-c.xyz','r')
oc3=oc2.read()
z2 = oc3.replace("H", "H   0")
oh.write(z2)
oh.close()
#**********************
oh2=open('out-h.xyz','r')
oh3=oh2.read()
z3 = oh3.replace("N", "N   0")
on.write(z3)
on.close()
#**********************
on2=open('out-n.xyz','r')
on3=on2.read()
z4 = on3.replace("O", "O   0")
oo.write(z4)
oo.close()
#**********************
os2=open('out-o.xyz','r')
os3=os2.read()
z5 = os3.replace("S", "S   0")
os.write(z5)
os.close()
#**********************************
oz2=open('out-s.xyz','r')
oz3=oz2.read()
z6 = oz3.replace("Zn", "Zn   0")
oz.write(z6)
oz.close()
#********************
#os.remove('out-c.xyz')
#os.remove('out-h.xyz')
#os.remove('out-n.xyz')
#os.remove('out-o.xyz')
#os.remove('out-s.xyz')
#**************************

# writing the header text

out3.write('%chk=blact-trunc-34.chk \n')
out3.write('%mem=3GB \n')
out3.write('%nproc=16 \n')
out3.write('#p opt(modredundant) b3lyp/gen nosymm guess=read pseudo=read scf=(conver=8,maxcycles=250) int=ultrafine \n \n')
out3.write('Title Card Required \n \n')
out3.write('0 1 \n')

# adding the coordinates
oz4=open('out-z.xyz','r')
for line in oz4:
       out3.write(line)


out3.close()
out2.close()

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



