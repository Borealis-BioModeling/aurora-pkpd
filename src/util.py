import streamlit as st

dosing_strategies = {
    "I.V. Bolus": "pkpd.dose_bolus",
    "I.V. Infusion": "pkpd.dose_infusion",
    "Oral": "pkpd.dose_absorbed",
}


def built_with(file):
    file.write("'''\n")
    file.write("Built with Aurora PK/PD.\n")
    file.write("'''\n")
    return


def standard_imports(file):
    file.write("from pysb import *\n")
    file.write("import pysb.pkpd as pkpd\n")
    file.write("\n")
    return


def new_model(file):
    file.write("##  Initialize the Model ## \n")
    file.write("Model()\n")
    file.write("\n")
    return


def compartments(file, comp_list):
    file.write("##  Compartments  ##\n")
    n_comp = len(comp_list)
    if n_comp == 1:
        file.write(
            'pkpd.one_compartment("{}", {}) \n'.format(
                comp_list[0]["name"], comp_list[0]["size"]
            )
        )
    elif n_comp == 2:
        file.write(
            'pkpd.two_compartments("{}", {}, "{}", {}) \n'.format(
                comp_list[0]["name"],
                comp_list[0]["size"],
                comp_list[1]["name"],
                comp_list[1]["size"],
            )
        )
    elif n_comp == 3:
        file.write(
            'pkpd.three_compartments("{}", {}, "{}", {}, "{}", {}) \n'.format(
                comp_list[0]["name"],
                comp_list[0]["size"],
                comp_list[1]["name"],
                comp_list[1]["size"],
                comp_list[2]["name"],
                comp_list[2]["size"],
            )
        )
    elif n_comp > 3:
        for i in range(n_comp):
            file.write("# Compartment {}".format(i + 1))
            file.write(
                'pkpd.one_compartment("{}", {}) \n'.format(
                    comp_list[i]["name"], comp_list[i]["size"]
                )
            )
    else:
        pass
    file.write("\n")
    return


def dose(file, drug_name, drug_dose, drug_compartment, dosing, dosing_kwargs):
    file.write("##  Drug & Dose  ##\n")
    file.write('pkpd.drug_monomer("{}") \n'.format(drug_name))
    dose_line = "{}({}, {}, {}".format(
        dosing_strategies[dosing], drug_name, drug_compartment, drug_dose
    )
    for item in dosing_kwargs.items():
        dose_line += ", {}={}".format(*item)
    dose_line += ") \n"
    file.write(dose_line)
    file.write("\n")
    return


def distribution(file, drug_name, distributions):
    file.write("##  Drug Distribution  ## \n")
    for dist in distributions:
        file.write(
            "pkpd.distribute({}, {}, {}, klist=[{}, {}]) \n".format(drug_name, *dist)
        )
    file.write("\n")


def elimination(file, drug_name, eliminations):
    file.write("##  Drug Elimination  ## \n")
    for elim in eliminations:
        file.write("pkpd.eliminate({}, {}, {}) \n".format(drug_name, *elim))
    file.write("\n")

def save_model_str(model_str):
    st.session_state.model_str = model_str

def save_model(model):
    st.session_state.model = model

def reload_saved_model():
    st.session_state.model.reload()