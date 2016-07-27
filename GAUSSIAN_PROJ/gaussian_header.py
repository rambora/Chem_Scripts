#!/usr/bin/python

output = 'gaussian4.com'
out3=open(output,'w')

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

#exit()  Should not exit here !!!!
