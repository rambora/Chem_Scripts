#!/usr/bin/python


import evb_quant_ave
import quant_evb_ave


LRA = 0.5 * (evb_quant_ave.evb_ene_diff + quant_evb_ave.quant_ene_diff)

print

print "LRA (EVB-->Quant):", LRA

