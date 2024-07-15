import streamlit as st
import os
import importlib.util
import sys
import tempfile

dosing_strategies = {
    "I.V. Bolus": "pkpd.dose_bolus",
    "I.V. Infusion": "pkpd.dose_infusion",
    "Oral": "pkpd.dose_absorbed",
}


PD_MODELS = {
    "Emax": "pkpd.emax",
    "Sigmoidal Emax": "pkpd.sigmoidal_emax",
    "Linear Effect": "pkpd.linear_effect",
    "Log-linear Effect": "pkpd.loglinear_effect",
    "Fixed-effect": "pkpd.fixed_effect",
}

PD_MODEL_EQS = {
    "Emax": r"E = E_{\textrm{max}} \frac{\left[\textrm{Drug}\right]}{\left[\textrm{Drug}\right] + EC_{\textrm{50}}}",
    "Sigmoidal Emax": r"E = E_{\textrm{max}} \frac{\left[\textrm{Drug}\right]^n}{\left[\textrm{Drug}\right]^n + EC_{\textrm{50}}^n}",
    "Linear Effect": r"E = m \left[\textrm{Drug}\right] + b",
    "Log-linear Effect": r"E = m \log(\left[\textrm{Drug}\right]) + b",
    "Fixed-effect": r"E = E_{\textrm{fixed}} \, \, , \, \left[\textrm{Drug}\right] > C_{\textrm{threshold}} \\ E = 0  \, \, , \, \left[\textrm{Drug}\right] \leq C_{\textrm{threshold}}",
}

def pd_emax_kwargs(drug_name, compartment):
    pd_kwargs = dict()
    pd_kwargs["emax"] = st.number_input(
        "Emax:",
        0.0,
        help="Maximum effect value.",
    )
    pd_kwargs["ec50"] = st.number_input(
        "EC50:",
        value=0.0,
        help="Drug concnetration at which the effect is 50% of Emax.",
    )
    return pd_kwargs

def pd_sigmoidal_emax_kwargs(drug_name, compartment):
    pd_kwargs = pd_emax_kwargs(drug_name, compartment)
    pd_kwargs["n"] = st.number_input(
        "n:",
        1.0,
        help="Hill coefficient.",
    )
    return pd_kwargs

def pd_linear_effect_kwargs(drug_name, compartment):
    pd_kwargs = dict()
    pd_kwargs["slope"] = st.number_input(
        "m:",
        1.0,
        help="Slope of the linear relationship.",
    )
    pd_kwargs["intercept"] = st.number_input(
        "b:",
        value=0.0,
        help="y-intercept of the linear relationship.",
    )
    return pd_kwargs

def pd_loglinear_effect_kwargs(drug_name, compartment):
    pd_kwargs = pd_linear_effect_kwargs(drug_name, compartment)
    return pd_kwargs

def pd_fixed_effect_kwargs(drug_name, compartment):
    pd_kwargs = dict()
    pd_kwargs["e_fixed"] = st.number_input(
        "Efixed:",
        0.0,
        help="The fixed-effect value.",
    )
    pd_kwargs["c_threshold"] = st.number_input(
        "$C_{threshold}$:",
        value=0.0,
        help="The drug threshold concentration above which there is an effect.",
    )
    return pd_kwargs

PD_MODEL_KWARGS = {
    "Emax": pd_emax_kwargs,
    "Sigmoidal Emax": pd_sigmoidal_emax_kwargs,
    "Linear Effect": pd_linear_effect_kwargs,
    "Log-linear Effect": pd_loglinear_effect_kwargs,
    "Fixed-effect": pd_fixed_effect_kwargs,
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
            file.write("# Compartment {} \n".format(i + 1))
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


def pd_model(file, drug_name, pd_model_name, pd_compartment, pd_kwargs):
    file.write("##  PD Model  ##\n")
    pd_line = "{}({}, {}".format(
        PD_MODELS[pd_model_name],
        drug_name,
        pd_compartment,
    )
    for item in pd_kwargs.items():
        pd_line += ", {}={}".format(*item)
    pd_line += ") \n"
    file.write(pd_line)
    file.write("\n")
    return

def observables(file, observe):
    file.write("##  Observables  ## \n")
    for obs in observe:
        file.write("Observable(\"obs_{}_{}\", {}()**{}) \n".format(*obs, *obs))
    file.write("\n")

def import_model():

    try:
        file_path = st.session_state.model_file
        module_name = "model"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        # return sys.modules[module_name]['model']
        return module.model
    except Exception as e:
        st.exception(e)
    return


def save_model_str(model_str):
    st.session_state.model_str = model_str


def save_model(model):
    st.session_state.model = model


def reload_saved_model():
    st.session_state.model.reload()


### pyvipr
import networkx as nx

# Special Keys
ID = "id"
NAME = "name"
DATA = "data"
ELEMENTS = "elements"

NODES = "nodes"
EDGES = "edges"

SOURCE = "source"
TARGET = "target"

DEF_SCALE = 100

CY_GML_NODE_STYLE = {"ellipse": "ellipse", "roundrectangle": "round-rectangle"}
CY_GML_ARROWS = {"standard": "triangle", "none": "none"}
CY_GML_LINE_STYLE = {"line": "solid", "dotted": "dotted", "dashed": "dashed"}


def to_networkx(cyjs, directed=True):
    """
    Convert Cytoscape.js-style JSON object into NetworkX object.
    By default, data will be handles as a directed graph.
    """

    if directed:
        g = nx.MultiDiGraph()
    else:
        g = nx.MultiGraph()

    network_data = cyjs[DATA]
    if network_data is not None:
        for key in network_data.keys():
            g.graph[key] = network_data[key]

    nodes = cyjs[ELEMENTS][NODES]
    edges = cyjs[ELEMENTS][EDGES]

    for node in nodes:

        data = node[DATA]
        if data["NodeType"] == "species":
            data["color"] = data["background_color"]
            data["group"] = data["parent"]
            data["level"] = 1
            # data["physics"] = False
        elif data["NodeType"] == "compartment":
            data["shape"] = "square"
            data["size"] = 150
            data["group"] = data["name"]
            data["level"] = 0
            data["physics"] = False
        # print(data)
        st.write(data)
        g.add_node(data[ID], **data)

    for edge in edges:
        data = edge[DATA]
        source = data[SOURCE]
        target = data[TARGET]

        g.add_edge(source, target, attr_dict=data)
        if data["source_arrow_shape"] == "triangle":
            g.add_edge(target, source, attr_dict=data)
    return g


def to_networkx_species(cyjs, directed=True):
    """
    Convert Cytoscape.js-style JSON object into NetworkX object.
    By default, data will be handles as a directed graph.
    """

    if directed:
        g = nx.MultiDiGraph()
    else:
        g = nx.MultiGraph()

    network_data = cyjs[DATA]
    if network_data is not None:
        for key in network_data.keys():
            g.graph[key] = network_data[key]

    nodes = cyjs[ELEMENTS][NODES]
    edges = cyjs[ELEMENTS][EDGES]

    for node in nodes:

        data = node[DATA]
        if data["NodeType"] == "species":
            data["color"] = data["background_color"]
            if "parent" in data:
                data["group"] = data["parent"]
            # data['level'] = 1
            # st.write(data)
            g.add_node(data[ID], **data)

    for edge in edges:
        data = edge[DATA]
        source = data[SOURCE]
        target = data[TARGET]

        g.add_edge(source, target, attr_dict=data)
        if data["source_arrow_shape"] == "triangle":
            g.add_edge(target, source, attr_dict=data)
    return g


def to_networkx_compartments(cyjs, directed=True):
    """
    Convert Cytoscape.js-style JSON object into NetworkX object.
    By default, data will be handles as a directed graph.
    """

    if directed:
        g = nx.MultiDiGraph()
    else:
        g = nx.MultiGraph()

    network_data = cyjs[DATA]
    if network_data is not None:
        for key in network_data.keys():
            g.graph[key] = network_data[key]

    nodes = cyjs[ELEMENTS][NODES]
    edges = cyjs[ELEMENTS][EDGES]

    for node in nodes:

        data = node[DATA]
        if data["NodeType"] == "compartment":
            data["shape"] = "box"
            # data['size'] = 150
            data["group"] = data["name"]
            data["level"] = 0
            data["physics"] = True
            # print(data)
            # st.write(data)
            g.add_node(data[ID], **data)

    for edge in edges:
        data = edge[DATA]
        source = data[SOURCE]
        target = data[TARGET]
        for node in nodes:
            node_data = node[DATA]
            if node_data["id"] == source:
                source_compartment = node_data["parent"]
            elif node_data["id"] == target:
                target_compartment = node_data["parent"]
        # st.write(data)
        g.add_edge(source_compartment, target_compartment, attr_dict=data)
        if data["source_arrow_shape"] == "triangle":
            g.add_edge(target_compartment, source_compartment, attr_dict=data)
    return g
