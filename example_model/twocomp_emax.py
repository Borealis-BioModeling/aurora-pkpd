'''
Built with Aurora PK/PD.
'''
from pysb import *
import pysb.units
from pysb.units import units
from pysb.pkpd import macros as pkpd
pysb.units.add_macro_units(pkpd)

with units():
    ##  Initialize the Model ## 
    Model()

    ##  Core Simulation Units  ##
    SimulationUnits(time="h", concentration="g / L", volume="L") 

    ##  Compartments  ##
    Parameter("V_CENTRAL", 1.0, unit="L") 
    Parameter("V_PERIPHERAL_1", 1.0, unit="L") 
    pkpd.two_compartments("CENTRAL", V_CENTRAL, "PERIPHERAL_1", V_PERIPHERAL_1) 

    ##  Drug & Dose  ##
    pkpd.drug_monomer("Imagiprofen") 
    Parameter("dose_Imagiprofen_CENTRAL", 0.09999999999999999, unit="g") 
    pkpd.dose_bolus(Imagiprofen, CENTRAL, dose_Imagiprofen_CENTRAL) 

##  Drug Distribution  ## 
    Parameter("kf_distribute_Imagiprofen_CENTRAL_PERIPHERAL_1", 0.1, unit=" 1 / h") 
    Parameter("kr_distribute_Imagiprofen_CENTRAL_PERIPHERAL_1", 0.05,  unit=" 1 / h") 
    pkpd.distribute(Imagiprofen, CENTRAL, PERIPHERAL_1, 
        klist=[kf_distribute_Imagiprofen_CENTRAL_PERIPHERAL_1,
               kr_distribute_Imagiprofen_CENTRAL_PERIPHERAL_1]) 

##  Drug Elimination  ## 
    Parameter("kel_Imagiprofen_CENTRAL", 0.1, unit=" 1 / h") 
    pkpd.eliminate(Imagiprofen, CENTRAL, kel_Imagiprofen_CENTRAL) 

##  PD Model  ##
    Parameter("Emax_emax_Imagiprofen_PERIPHERAL_1", 10.0) 
    Unit(Emax_emax_Imagiprofen_PERIPHERAL_1, None) 
    Parameter("Emax_ec50_Imagiprofen_PERIPHERAL_1", 0.01, unit="g / L") 
    pkpd.emax(Imagiprofen, PERIPHERAL_1, emax=Emax_emax_Imagiprofen_PERIPHERAL_1, ec50=Emax_ec50_Imagiprofen_PERIPHERAL_1) 

    ##  Observables  ## 
    Observable("obs_Imagiprofen_CENTRAL", Imagiprofen()**CENTRAL) 
    Observable("obs_Imagiprofen_PERIPHERAL_1", Imagiprofen()**PERIPHERAL_1) 

