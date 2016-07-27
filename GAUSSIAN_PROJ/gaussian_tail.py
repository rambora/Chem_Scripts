#!/usr/bin/python

output = 'gaussian4.com'

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

#exit()
# appending the above data text at the end of a file
