#!/usr/bin/python

out2=open('gau1.com','r')
 
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

out2.close()

#exit()
