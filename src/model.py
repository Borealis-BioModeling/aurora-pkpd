from pysb import *
import pysb.pkpd as pkpd

##  Initialize the Model ## 
Model()

##  Compartments  ##
pkpd.one_compartment("CENTRAL", 1.0) 

##  Drug & Dose  ##
pkpd.drug_monomer("Imagiprofen") 
pkpd.dose_bolus(Imagiprofen, 0.0) 

