#! /usr/bin/env python
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

#print clock(), time()
t1=time()
help = """
This python script requires 5 mandatory parameters and 1 optional:
--qm_prog=string (quantum program to be used; currently only g03 is supported)
--qm_method=string (string containing ai method, e.g. 'b3lyp/6-31+G*')
--file_in=string (file created by molaris)
--file_out=string (file created by this script that will be read by molaris)
--qm_inp=string (name of the input file for ab initio program)
--e_ref=float (reference energy [a.u.] for the quantum system)
[--xmov=string] (optional; name of the file where xyz movie will be stored)"""

try:
    opts,args = getopt.getopt(sys.argv[1:],'',['qm_prog=','file_in=', 'qm_method=' , 'file_out=','qm_inp=','e_ref=','xmov=','BASIS=','EXCHANGE=','CORR=','CHRG-MULT=','RAND_ID=','mpifile='])
except getopt.error:
    print help
    sys.exit(2)

file_xyz = '';                              # by default do NOT store xyz snapshots of the regI
for o,a in opts:
    if o == '--qm_prog':
        qm_prog = a
    if o == '--qm_method':
        qm_method = a
    if o == '--file_in':
        file_in = a
    if o == '--file_out':
        file_out = a
    if o == '--qm_inp':
        qm_inp = a
    if o == '--e_ref':
        e_ref = float(a)
    if o == '--CHRG-MULT':
        CHARGE = a
    if o == '--xmov':
        file_xyz = a
    if o == '--RAND_ID':
        rand_flag = a
    if o == '--mpifile':
        mpifile = a
#file_ESP = 'ESPGrid'  #for QChem for writing the grid for ESP 
regI_full = []
regI_frozen = []
regI_w = []
regII_p = []
regII_w = []

file_in_fh = open(file_in,'r')              # process the first line of the file_in
items = split(file_in_fh.readline())
md_step = int(items[0])
etot = float(items[1])
evdw_12 = float(items[2])
ea = float(items[3])
eb = float(items[4])
edft_elec = float(items[5])
edft_vdw = float(items[6])
force_flag = int(items[7])
#print force_flag
#force_flag = 0			#TEMP FEB 12 12

items = split(file_in_fh.readline())
n_regI_full = int(items[0])        # read region I atoms 
n_regI_link = int(items[1]) 
####n_regI_frozen = int(items[0]) 
n_regI_w = int(items[0]) 
n_regII_p = int(items[0]) 
n_regII_w = int(items[0]) 

n_regI = n_regI_link + n_regI_full
for i in range(0, n_regI):
    line = file_in_fh.readline()
    items = split(line)   # atom name, x, y, z and crg
    #regI_full.append(items[0], float(items[1]), float(items[2]),\
    #          float(items[3]), float(items[4]))
    pp=[]
    pp.append(items[0])
    for j in range(1,5):
       pp.append(float(items[j]))
    regI_full.append(pp)

n_regI_frozen = int(split(file_in_fh.readline())[0]) # read protein atoms from frozen region I'
for i in range(0,n_regI_frozen):                     # (TODO: treat the groups in region I' properly)
    line = file_in_fh.readline()                          
    items = split(line)   # atom name, x, y, z and crg
    #regI_frozen.append(items[0], float(items[1]), float(items[2]),\
    #    float(items[3]), float(items[4]))
    pp=[]
    pp.append(items[0])
    for j in range(1,5):
       pp.append(float(items[j]))
    regI_frozen.append(pp)

n_regI_w = int(split(file_in_fh.readline())[0])           # read water molecules from frozen region I'
for i in range(0, n_regI_w):
    line = file_in_fh.readline()
    items = split(line)   # atom name, x, y, z and crg
    #regI_w.append(items[0], float(items[1]), float(items[2]),\
    #    float(items[3]), float(items[4]))
    pp=[]
    pp.append(items[0])
    for j in range(1,5):
       pp.append(float(items[j]))
    regI_w.append(pp)

n_regII_p = int(split(file_in_fh.readline())[0])           # read protein atoms from region II
for i in range(0, n_regII_p):
    line = file_in_fh.readline()
    items = split(line)   # atom name, x, y, z and crg
    #regII_p.append(items[0], float(items[1]), float(items[2]),\
    #    float(items[3]), float(items[4]))
    pp=[]
    pp.append(items[0])
    for j in range(1,5):
       pp.append(float(items[j]))
    regII_p.append(pp)

n_regII_w = int(split(file_in_fh.readline())[0])           # read water molecules from region II
for i in range(0, n_regII_w):
    line = file_in_fh.readline()
    items = split(line)   # atom name, x, y, z and crg
    #regII_w.append(items[0], float(items[1]), float(items[2]),\
    #    float(items[3]), float(items[4]))
    pp=[]
    pp.append(items[0])
    for j in range(1,5):
       pp.append(float(items[j]))
    regII_w.append(pp)
                                                     
crg_regI_full = 0.0                                  # determine the total charges qm regions
for a in regI_full:
    name, x, y, z, crg = a
    crg_regI_full = crg_regI_full + crg
crg_regI_full = int(round(crg_regI_full))

crg_regI_frozen = 0.0
for a in regI_frozen:
    name, x, y, z, crg = a
    crg_regI_frozen = crg_regI_frozen + crg
crg_regI_frozen = int(round(crg_regI_frozen))

crg_regI_w = 0.0
for a in regI_w:
    name, x, y, z, crg = a
    crg_regI_w = crg_regI_w + crg
crg_regI_w = int(round(crg_regI_w))

# Run the QM job
if qm_prog == 'g03':                                 # create input for gaussian 98
#    print 'USING G03 program'
#    print 'MP-based CORRELATION METHODS not implemented' #MP2-4, CCSD it reads SCF Energy, while \MP2=, \CCSD= is needed 
    if len(regII_p) > 0 or len(regII_w) > 0:         # (TODO: treat the groups in frozen region properly) 
        ext_crg_keyw = ' charge'
    else:
        ext_crg_keyw = ''
        ext_crg = 0.0
    if force_flag:
        force_keyw = ' force '
    else:
        force_keyw = ' '
    qm_inp_fh = open(qm_inp, 'w')
    qm_inp_fh.write('%NProc=8\n')
#    qm_inp_fh.write('%NProcShared=4\n')
#    qm_inp_fh.write('%NProcLinda=4\n')
    qm_inp_fh.write('%MEM=8GB\n')

    qm_inp_fh.write('%Chk=/tmp/Check.file'+rand_flag+'\n')
#    if  not os.path.exists('Check.file') :
    if md_step == 0:
        qm_inp_fh.write('#'+qm_method+ext_crg_keyw+force_keyw+'pop=(mk) NoSymm SCF=(Conver=5)\n')
#        qm_inp_fh.write('#'+qm_method+ext_crg_keyw+force_keyw+'NoSymm SCF=(Conver=5)\n')
    else:
        qm_inp_fh.write('#'+qm_method+ext_crg_keyw+force_keyw+'pop=(mk) Guess=Read NoSymm SCF=(Conver=5)\n')
#        qm_inp_fh.write('#'+qm_method+ext_crg_keyw+force_keyw+'Guess=Read NoSymm SCF=(Conver=5)\n')
    qm_inp_fh.write('\n')
    qm_inp_fh.write('snapshot of MD step %d\n' % md_step) 
    qm_inp_fh.write('\n')
#    qm_inp_fh.write('%d 1\n' % (crg_regI_full + crg_regI_frozen + crg_regI_w,))
# hardcoded -4 charge 
    qm_inp_fh.write(CHARGE+'\n')
    for a in regI_full:
        name, x, y, z, crg = a
        qm_inp_fh.write('%s  %15.10f %15.10f %15.10f\n' % (name, x, y, z))
    for a in regI_frozen:
        name, x, y, z, crg = a
        qm_inp_fh.write('%s  %15.10f %15.10f %15.10f\n' % (name, x, y, z))
    for a in regI_w:
        name, x, y, z, crg = a
        qm_inp_fh.write('%s  %15.10f %15.10f %15.10f\n' % (name, x, y, z))
    qm_inp_fh.write('\n')
    for a in regII_p:
        name, x, y, z, crg = a
        qm_inp_fh.write('%15.10f %15.10f %15.10f %10.3f\n' % (x, y, z, crg))
    for a in regII_w:
        name, x, y, z, crg = a
        qm_inp_fh.write('%15.10f %15.10f %15.10f %10.3f\n' % (x, y, z, crg))
    qm_inp_fh.write('\n')
    qm_inp_fh.close()
                                                     # run the g03 job
    system('cd ' + os.path.split(qm_inp)[0] + '; g03 ' + qm_inp)
#    system('cd ' + os.path.split(qm_inp)[0] + '; ' + qm_prog + ' ' + qm_inp)
    # system('g03 ' + qm_inp)
# Job cpu time:  0 days  0 hours  1 minutes  3.0 seconds.
# File lengths (MBytes):  RWF=    136 Int=      0 D2E=      0 Chk=     20 Scr=      1
# Normal termination of Gaussian 03 at Thu Nov 29 12:59:39 2012.
    qm_out_fh =  open('qm.log', 'r')
    line = qm_out_fh.readline()
    while line:
     if re.compile(' Job cpu time').match(line):
                print line
     line = qm_out_fh.readline()
     if re.compile(' Normal termination of Gaussian').match(line):
                print line
		break
    qm_out_fh.close()
#TEST FOR QCHEM NIKO
elif qm_prog == 'qchem':                                 # create input for QChem
    print 'USING QChem4 program'
    if len(regII_p) > 0 or len(regII_w) > 0:         # (TODO: treat the groups in frozen region properly) 
        ext_crg_keyw = 'external_charges'
    else:
        ext_crg_keyw = ''
        ext_crg = 0.0
    if force_flag:
        force_keyw = 'FORCE'
    else:
        force_keyw = 'SP'
    qm_inp_fh = open(qm_inp, 'w')
    qm_inp_fh.write('$comment\n')
    qm_inp_fh.write('snapshot of MD step %d\n' % md_step)
    qm_inp_fh.write('$end\n')
    qm_inp_fh.write('\n')
# $rem options
    qm_inp_fh.write('$rem\n')
    qm_inp_fh.write('JOBTYPE '+force_keyw+'\n')
    qm_inp_fh.write('QM_MM TRUE\n')
    qm_inp_fh.write('QMMM_PRINT TRUE\n')
    qm_inp_fh.write('EXCHANGE '+qm_method+'\n')
    qm_inp_fh.write('MEM_TOTAL 1500\n')
#    qm_inp_fh.write('MEM_STATIC 1400\n')
#    qm_inp_fh.write('MAX_SUB_FILE_NUM 32\n')
#    qm_inp_fh.write('AO2MO_DISK 66000\n')
#    qm_inp_fh.write('CORRELATION LYP\n')
#    qm_inp_fh.write('CORRELATION CCSD\n')
#    qm_inp_fh.write('BASIS CC-PVDZ\n')
    qm_inp_fh.write('SCF_CONVERGENCE 5\n')
    if md_step > 0:
        qm_inp_fh.write('SCF_GUESS READ\n')

    qm_inp_fh.write('THRESH 8\n')
    qm_inp_fh.write('BASIS 6-31G*\n')
#    qm_inp_fh.write('N_FROZEN_CORE FC\n')
#    qm_inp_fh.write('POP_MULLIKEN FALSE\n')
    qm_inp_fh.write('SYMMETRY OFF\n')
    qm_inp_fh.write('SYM_IGNORE TRUE\n')
#    qm_inp_fh.write('ESP_CHARGES TRUE\n')
#    qm_inp_fh.write('CC_SYMMETRY 0\n')
##    if force_flag:
##	    qm_inp_fh.write('IGDEFIELD 2\n')
##	    qm_inp_fh.write('IGDESP %d\n' % (n_regII_p+n_regII_w))
    qm_inp_fh.write('$end\n')
    qm_inp_fh.write('\n')
# $molecule specification
    qm_inp_fh.write('$molecule\n') 
    qm_inp_fh.write(CHARGE+'\n')
    for a in regI_full:
        name, x, y, z, crg = a
        qm_inp_fh.write('%s  %15.10f %15.10f %15.10f\n' % (name, x, y, z))
    for a in regI_frozen:
        name, x, y, z, crg = a
        qm_inp_fh.write('%s  %15.10f %15.10f %15.10f\n' % (name, x, y, z))
    for a in regI_w:
        name, x, y, z, crg = a
        qm_inp_fh.write('%s  %15.10f %15.10f %15.10f\n' % (name, x, y, z))
    qm_inp_fh.write('$end\n')
    qm_inp_fh.write('\n')
# $external_charges
    if len(regII_p) > 0 or len(regII_w) > 0:
     qm_inp_fh.write('$'+ext_crg_keyw+'\n')
#    qchem_esp_grid = open(file_ESP, 'w')
     for a in regII_p:
        name, x, y, z, crg = a
        qm_inp_fh.write('%15.10f %15.10f %15.10f %10.3f\n' % (x, y, z, crg))
#	qchem_esp_grid.write('%15.10f %15.10f %15.10f\n' % ((x/0.529177),(y/0.529177),(z/0.529177)))
     for a in regII_w:
        name, x, y, z, crg = a
        qm_inp_fh.write('%15.10f %15.10f %15.10f %10.3f\n' % (x, y, z, crg))
#	qchem_esp_grid.write('%15.10f %15.10f %15.10f\n' % ((x/0.529177),(y/0.529177),(z/0.529177)))
#    qchem_esp_grid.close()
     qm_inp_fh.write('$end\n')
    qm_inp_fh.write('\n')
    qm_inp_fh.close()
                                                     # run the qchem job
#    print 'cd ' + os.path.split(qm_inp)[0] + '; ' + qm_prog + ' ' + qm_inp + ' QChem.out'
#    system('cd ' + os.path.split(qm_inp)[0] + '; rm efield.dat')
#    system('echo $PBS_VNODENUM')
#    system('ompi_info --param mpi all')
    system('cd ' + os.path.split(qm_inp)[0] + '; mpirun --hostfile nodefile -np 8 '+ qm_prog + ' ' + qm_inp + ' QChem.out saveme'+rand_flag)
#    system('cd ' + os.path.split(qm_inp)[0] + '; mpirun --prefix /soft/openmpi/1.4.3/intel12 --hostfile nodefile -np 8 '+ qm_prog + ' ' + qm_inp + ' QChem.out saveme'+rand_flag)
#    system('cd ' + os.path.split(qm_inp)[0] + '; ' + qm_prog + ' ' + qm_inp + ' QChem.out saveme$PBS_VNODENUM')
    if md_step%100 == 0:
	    system('cat '+qm_inp+'>>QCHEM_TEMP')
	    system('echo "      " >>QCHEM_TEMP')
	    system('echo "@@@" >>QCHEM_TEMP')
	    system('echo "      " >>QCHEM_TEMP')
#    system('cd ' + os.path.split(qm_inp)[0] + '; mpirun -np 12 --mca rmaps_base_schedule_policy node ' + qm_prog + ' ' + qm_inp + ' QChem.out')
#    system('cd ' + os.path.split(qm_inp)[0] + '; ' + qm_prog + ' -np 8 ' + qm_inp + ' QChem.out')
    qm_out_fh =  open('QChem.out', 'r')
    line = qm_out_fh.readline()                      
    print line
    c_flag = 0 
    while line:
#        if re.compile('\W+\*+  Thank you very').match(line):
        if re.compile(' Total job time').match(line):
		print line
		c_flag = 1
		if force_flag:
			 system('tail -'+str(n_regI + n_regI_frozen + n_regI_w)+' efield.dat > force.out')
		break
        line = qm_out_fh.readline()
    qm_out_fh.close()
    if c_flag != 1:
	print "QCHEM CRUSHED, ATTEMPTING TO RESTART"
	system('cp QChem.out QChem_crush.out')
	system('sed s/SCF_GUESS/\!SCF_GUESS/ QChem.inp > QChem_crush.inp')
	system('mv QChem_crush.inp QChem.inp')
#	system('cd ' + os.path.split(qm_inp)[0] + '; ' + qm_prog + ' QChem.inp QChem.out saveme$PBS_VNODENUM')
#        system('cd ' + os.path.split(qm_inp)[0] + '; mpirun -np 12 --mca rmaps_base_schedule_policy node ' + qm_prog + ' ' + qm_inp + ' QChem.out')
#        system('cd ' + os.path.split(qm_inp)[0] + '; mpirun -np 8 ' + qm_prog + ' ' + qm_inp + ' QChem.out')
        system('cd ' + os.path.split(qm_inp)[0] + '; mpirun --hostfile nodefile -np 8 '+ qm_prog + ' ' + qm_inp + ' QChem.out saveme'+rand_flag)
	qm_out_fh =  open('QChem.out', 'r')
    	line = qm_out_fh.readline()
    	print line
    	c_flag = 0
    	while line:
#        	if re.compile('\W+\*+  Thank you very').match(line):
		if re.compile(' Total job time').match(line):
                	print line
                	c_flag = 1
                	if force_flag:
                        	 system('tail -'+str(n_regI + n_regI_frozen + n_regI_w)+' efield.dat > force.out')
                	break
        	line = qm_out_fh.readline()
	qm_out_fh.close()
    	if c_flag != 1:
        	print "ATTEMPT to RERUN FAILED"
		sys.exit(2)
	else:
        	print "RESTART SUCCEEDED"
	
#    call(['ls', '-l'])
#    call('if ( ! { grep -s "Thank you very" QChem.out } ) echo "abnormal qchem run"')
#    print 'if ( ! { grep -s "Thank you very" QChem.out } ) echo "abnormal qchem run"'
#    system('if ( ! { grep -s "Thank you very" QChem.out } ) echo "abnormal qchem run"')
#    system('if ( ! { grep -s "Thank you very" QChem.out } ) sleep 30')
#    system('if ( ! { grep -s "Thank you very" QChem.out } ) qchem QChem.inp QChem.out')
#    if force_flag:
#    	system('echo "CARTESIAN COMPONENTS OF FORCES" >> QChem.out')
#    	print 'tail -'+str(n_regI + n_regI_frozen + n_regI_w)+' efield.dat >> QChem.out'
#    	system('tail -'+str(n_regI + n_regI_frozen + n_regI_w)+' efield.dat >> QChem.out')
#    system('cd ' + os.path.split(qm_inp)[0] + '; mpirun -np 1 ' + qm_prog + ' ' + qm_inp + ' QChem.out')
#mpirun -np 1 qchem $name.inp $name.out
    print 'QChem run completed'
    # system('qchem ' + qm_inp)
#TEST FOR QCHEM
elif qm_prog == 'mopac':
    if force_flag:
        force_keyw = ' GRAD '
    else:
	force_keyw = ' '

    qm_inp_fh = open(qm_inp, 'w')

    qm_inp_fh.write(qm_method+' 1SCF CHARGE='+CHARGE+' SINGLET'+force_keyw+'LET XYZ DEBUG MOL_QMMM'+' \n')
#    EPS=78.4 PRECISE
#    qm_inp_fh.write(qm_method+' 1SCF CHARGE='+CHARGE+' SINGLET'+force_keyw+'LET XYZ ESP'+' \n')
#    qm_inp_fh.write(qm_method+' 1SCF CHARGE='+CHARGE+' SINGLET EPS=78.4 PRECISE'+force_keyw+'LET XYZ'+' \n')
    qm_inp_fh.write('snapshot of MD step %d\n' % md_step)
    qm_inp_fh.write('\n')
    for a in regI_full:
        name, x, y, z, crg = a
        qm_inp_fh.write('%s  %15.10f %s %15.10f %s %15.10f %s\n' % (name, x, ' 1', y, ' 1', z, ' 1'))
#    for a in regI_frozen:
#        name, x, y, z, crg = a
#        qm_inp_fh.write('%s  %15.10f %15.10f %15.10f\n' % (name, x, y, z))
#    for a in regI_w:
#        name, x, y, z, crg = a
#        qm_inp_fh.write('%s  %15.10f %15.10f %15.10f\n' % (name, x, y, z))
#    qm_inp_fh.write('\n')
#    for a in regII_p:
#        name, x, y, z, crg = a
#        qm_inp_fh.write('%15.10f %15.10f %15.10f %10.3f\n' % (x, y, z, crg))
#    for a in regII_w:
#        name, x, y, z, crg = a
#        qm_inp_fh.write('%15.10f %15.10f %15.10f %10.3f\n' % (x, y, z, crg))
    qm_inp_fh.write('\n')
    qm_inp_fh.close()
                                                     # run the mopac job
    system('cd ' + os.path.split(qm_inp)[0] + '; $mopac ' + qm_inp)
#    system('cd ' + os.path.split(qm_inp)[0] + '; ' + '/auto/rcf-proj3/aw/plotniko/MOPAC2009/MOPAC2009.exe' + ' ' + qm_inp)
#    system('echo "1" > /auto/rcf-40/plotniko/.history')

#external call to MOLARIS
elif qm_prog == '/auto/rcf-proj3/aw/plotniko/MOLARIS9.11/molaris_hpc9.11':
#    qm_inp_fh = open(qm_inp, 'w')
    system('cd ' + os.path.split(qm_inp)[0] + '; cat temp > ' + qm_inp )
    system(qm_prog + ' < ' + qm_inp + ' > Molaris.out')	
else:
    print 'ERROR: Input file format for ' + qm_prog + ' ab initio package not implemented.'
    sys.exit(2)

# Read the results of the QM job 
if qm_prog == 'g03':                                 # (TODO: treat groups in frozen regions)
    print 'READING G03 ouput'
    qm_out_fh =  open(splitext(qm_inp)[0]+'.log', 'r')
    e_selfcrg = 0.0
    line = qm_out_fh.readline()                      # read energy
    while line:
        if re.compile(' Self energy of the charges').match(line):
            e_selfcrg = float(split(line)[6])
        if re.compile(' SCF Done').match(line):
            e_scf=float(split(line)[4])
            print 'Eref = ',e_ref, 'Eself = ', e_selfcrg, ' E SCF = ',e_scf
            e_qm = (e_scf - e_selfcrg - e_ref)* 627.509469
            break
        line = qm_out_fh.readline()

    espcrg = []                                      # read ESP fitted charges
    line = qm_out_fh.readline()
    while line:
#        if re.compile(' Charges from ESP fit').match(line):
#            line = qm_out_fh.readline()
#            line = qm_out_fh.readline()
        if re.compile(' Mulliken atomic charges').match(line):
            line = qm_out_fh.readline()
            for i in range(0, n_regI + n_regI_frozen + n_regI_w):
                line = qm_out_fh.readline()
                items = split(line)
                espcrg.append(float(items[2]))
            break
        line = qm_out_fh.readline()

    forces = []                                      # read forces
    f2kcal = 627.509469 / 0.529177
    line = qm_out_fh.readline()
    while line:
        if re.compile(' Center     Atomic                   Forces').match(line):
            line = qm_out_fh.readline()
            line = qm_out_fh.readline()
            for i in range(0, n_regI + n_regI_frozen + n_regI_w):
                line = qm_out_fh.readline()
                items = split(line)
                if force_flag:
                    pp=[]
                    for j in range(2,5):
                         pp.append(float(items[j])*f2kcal)
                    forces.append(pp)
                    #forces.append((float(items[2])*f2kcal, float(items[3])*f2kcal, 
                    #    float(items[4])*f2kcal))
#                else:
#                    forces.append(0.0, 0.0, 0.0)
            break
#        else:
#            for i in range(0, n_regI + n_regI_frozen + n_regI_w):
#                forces.append(0.0, 0.0, 0.0)
#            break 
        line = qm_out_fh.readline()
    qm_out_fh.close()
###QChem test
elif qm_prog == 'qchem':                                 # (TODO: treat groups in frozen regions)
    print 'READING QChem ouput'
#    qm_out_fh =  open(splitext(qm_inp)[0]+'.out', 'r')
    qm_out_fh =  open('QChem.out', 'r')
    e_selfcrg = 0.0
    line = qm_out_fh.readline()                      # read energy
    if len(regII_p) > 0 or len(regII_w) > 0:
      while line:
        if re.compile(' Charge-charge energy').match(line):
            e_selfcrg = float(split(line)[3])
	    break
        line = qm_out_fh.readline()

#        if re.compile('CCSD Total Energy').match(line):
#N        if re.compile(' The QM part of the Energy is').match(line):
#N	    print line
#        if re.compile('        MP2         total energy').match(line):
#            e_scf=float(split(line)[4])
#N            e_scf=float(split(line)[7])
#N            print 'Eref = ',e_ref, 'Eself = ', e_selfcrg, ' E SCF = ',e_scf
#N            e_qm = (e_scf - e_selfcrg - e_ref)* 627.509469
#N            break
#N        line = qm_out_fh.readline()

    espcrg = []                                      # read ESP fitted charges
    line = qm_out_fh.readline()
#    print 'READING Mulliken Charges'
    while line:
        if re.compile('          Ground-State Mulliken Net Atomic Charges').match(line):
#        if re.compile('         Merz-Kollman ESP Net Atomic Charges').match(line):
#	    print line
            line = qm_out_fh.readline()
            line = qm_out_fh.readline()
            line = qm_out_fh.readline()
#	    print line
            for i in range(0, n_regI + n_regI_frozen + n_regI_w):
                line = qm_out_fh.readline()
                items = split(line)
#		print items[0], items[2]
                espcrg.append(float(items[2]))
            break
        line = qm_out_fh.readline()
#NEW PLACE
    line = qm_out_fh.readline()
    while line:
        if re.compile(' The QM part of the Energy is').match(line):
#            print line
            e_scf=float(split(line)[7])
            print qm_method, md_step, 'Eself = ', e_selfcrg, ' E SCF = ',e_scf
            e_qm = (e_scf - e_selfcrg - e_ref)* 627.509469
            break
        line = qm_out_fh.readline()
#END
    qm_out_fh.close()
    if force_flag:
	    qm_out_fh2 =  open('force.out', 'r')

#N    dim = (n_regI + n_regI_frozen + n_regI_w)

	    forces = []                                      # read forces
	    f2kcal = -627.509469 / 0.529177
#NEW
	    for i in range(0, n_regI + n_regI_frozen + n_regI_w):
		line = qm_out_fh2.readline()
		items = split(line)
		pp=[]
		for j in range(0,3):
			pp.append(float(items[j])*f2kcal)
		forces.append(pp)
	    qm_out_fh2.close()
#NEW
	    	
#    line = qm_out_fh2.readline()

#N    numb_atom = 5 #TESTED for CCSD job in QChem
#    while line:
#       if re.compile('CARTESIAN COMPONENTS OF FORCES').match(line):
#            print 'READING FORCES copied from efield.dat'
#            for i in range(0, n_regI + n_regI_frozen + n_regI_w):
#                line = qm_out_fh.readline()
#                items = split(line)
#                if force_flag:
#                    pp=[]
#                    for j in range(0,3):
#                         pp.append(float(items[j])*f2kcal)
#                    forces.append(pp)
#		    print pp
#            break
#       line = qm_out_fh.readline()
#QChem test
elif qm_prog == 'mopac':
    qm_out_fh =  open(splitext(qm_inp)[0]+'.out', 'r')
    e_selfcrg = 0.0
    line = qm_out_fh.readline()                      # read energy
    while line:
        if re.compile('          FINAL HEAT OF FORMATION').match(line):
            e_scf=float(split(line)[5])
            e_qm = (e_scf - e_ref)
	    if (md_step%5 == 0) and (md_step > 0):
		 print qm_method, md_step, ' E SCF POLAR= ',e_scf
            break
        line = qm_out_fh.readline()

    forces = []                                      # read forces
    f2kcal = -1.0
    line = qm_out_fh.readline()
    if force_flag:
      while line:
        if re.compile('       FINAL  POINT  AND  DERIVATIVES').match(line):
            line = qm_out_fh.readline()
            line = qm_out_fh.readline()
#	    print 'PRINTING FORCES FROM python'
            for i in range(0, n_regI + n_regI_frozen + n_regI_w):

               	if force_flag:
		  pp=[]
		  for j in range(0,3):
                    line = qm_out_fh.readline()
                    items = split(line)
#                   print line
#		    print 'j=', j
                    pp.append(float(items[6])*f2kcal)
                  forces.append(pp)
#       		  print pp
 
            break
        line = qm_out_fh.readline()


    espcrg = []                                      # read ESP fitted charges
    line = qm_out_fh.readline()
    while line:
#        if re.compile('            ELECTROSTATIC POTENTIAL CHARGES').match(line):	#DOESNT EXIST FOR PM6
        if re.compile('              NET ATOMIC CHARGES AND DIPOLE CONTRIBUTIONS').match(line):
            line = qm_out_fh.readline()
            line = qm_out_fh.readline()
            for i in range(0, n_regI + n_regI_frozen + n_regI_w):
                line = qm_out_fh.readline()
                items = split(line)
                espcrg.append(float(items[2]))
#		print i,'Q=',espcrg[i]
            break
        line = qm_out_fh.readline()
    qm_out_fh.close()
elif qm_prog == '/auto/rcf-proj3/aw/plotniko/MOLARIS9.11/molaris_hpc9.11':
    qm_out_fh =  open(splitext(qm_inp)[0]+'.out', 'r')
    espcrg = []                                      # read ESP fitted charges
    line = qm_out_fh.readline()
    while line:
        if re.compile(' EVB Adiabatic charges').match(line):
            for i in range(0, n_regI_full):
                line = qm_out_fh.readline()
                items = split(line)
                espcrg.append(float(items[4]))
#                print i,'Q=',espcrg[i]
            break
        line = qm_out_fh.readline()


    e_selfcrg = 0.0
    line = qm_out_fh.readline()                      # read energy
    while line:
        if re.compile(' ENZ_NOF: Eg through eoff').match(line):
            e_scf=float(split(line)[4])
#            print 'Eref = ',e_ref, 'Eself = ', e_selfcrg, ' E SCF = ',e_scf
            e_qm = (e_scf - e_ref)
            break
        line = qm_out_fh.readline()

    forces = []                                      # read forces
    f2kcal = -1.0
    line = qm_out_fh.readline()
    if force_flag:
      while line:
        if re.compile('ENERGY DERIVATIVES FROM MOLARIS AS QM').match(line):
#            print 'PRINTING FORCES FROM python'
            for i in range(0, n_regI_full):

                if force_flag:
                  pp=[]
                  line = qm_out_fh.readline()
                  for j in range(1,4):
                    items = split(line)
#                    print line
#                    print 'j=', j
                    pp.append(float(items[j])*f2kcal)
                  forces.append(pp)
#                         print pp

            break
        line = qm_out_fh.readline()


    qm_out_fh.close()
else:
    print 'ERROR: Output file format of ' + qm_prog + ' ab initio package not implemented.'
    sys.exit(2)

# Create the file_out that will be read by MOLARIS
file_out_fh = open(file_out, 'w')
file_out_fh.write('%25.10f\n' % e_qm)
if force_flag:
	for f in forces:
	    x,y,z=f
	    file_out_fh.write('%15.10f %15.10f %15.10f\n' % (x,y,z))
#	    print x/f2kcal,y/f2kcal,z/f2kcal
else:
	for i in range(0, n_regI + n_regI_frozen + n_regI_w):
		dummy=0.0
		file_out_fh.write('%15.10f %15.10f %15.10f\n' % (dummy,dummy,dummy))
#for c in espcrg:
#    file_out_fh.write('%8.4f\n' % c)
file_out_fh.close()
if file_xyz != '':
    file_xyz_fh = open(file_xyz, 'a+')
    file_xyz_fh.write('%d\n' % (n_regI + n_regI_frozen + n_regI_w,))
    file_xyz_fh.write('step: %d %12.5f %12.5f\n' % (md_step,e_qm,etot))
    for a in regI_full:
        name, x, y, z, crg = a
        file_xyz_fh.write('%s  %15.10f %15.10f %15.10f\n' % (name, x, y, z))
    for a in regI_frozen:
        name, x, y, z, crg = a
        file_xyz_fh.write('%s  %15.10f %15.10f %15.10f\n' % (name, x, y, z))
    for a in regI_w:
        name, x, y, z, crg = a
        file_xyz_fh.write('%s  %15.10f %15.10f %15.10f\n' % (name, x, y, z))
    file_xyz_fh.close()
#print clock(), time()
t2=time()
dt=t2-t1
print 'time for QM call with',qm_prog,dt
