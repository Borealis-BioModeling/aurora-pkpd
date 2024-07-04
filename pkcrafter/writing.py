
dosing_strategies = {
    "I.V. Bolus": 'pkpd.dose_bolus',
    "I.V. Infusion": 'pkpd.dose_infusion',
    "Oral": 'pkpd.dose_absorbed',
}

def standard_imports(file):
    file.write("from pysb import *\n")
    file.write("import pysb.pkpd as pkpd\n")
    file.write("\n")
    return