import streamlit as st
from importlib.metadata import version
import util
import os
import importlib.util
import sys

compartment_counts = {"one": 1, "two": 2, "three": 3}


# col1, col2, col3 = st.columns(3)
# with col2:
#     st.header("Model Builder")
st.title("Model Builder")
# with col3:
#     st.image("https://avatars.githubusercontent.com/u/163594810?s=200&v=4", width=100)

st.text(
    "Build and export compartmental PK (pharmacokinetics) models in the PySB format."
)

st.write(" ")
st.markdown("------")

# st.markdown("### 1. Name The Model")
# model_name = st.text_input("Model Name:", "pkmodel")
model_name = "model"
model_dir = ".model/"

# st.write(" ")
# st.markdown("------")

st.markdown("### 1. Define the Compartments")

compartments = []
n_comp = 1
# num_compartment = st.radio("Number of Compartments:", ["one", "two", "three", "more"])
# if num_compartment == "more":
n_comp = st.number_input("Number of Compartments:", value=1, min_value=1, step=1)
# else:
#    n_comp = compartment_counts[num_compartment]

for i in range(n_comp):
    compartments.append({})
    st.write("Compartment  {}".format(i + 1))
    if i == 0:
        cols = st.columns(2)
        compartments[i]["name"] = cols[0].text_input("Name:", "CENTRAL")
        compartments[i]["size"] = cols[1].number_input(
            "Size:", value=1.0, min_value=0.0, key="COMP_SIZE_{}".format(i)
        )
    else:
        cols = st.columns(2)
        compartments[i]["name"] = cols[0].text_input("Name:", "PERIPHERAL_{}".format(i))
        compartments[i]["size"] = cols[1].number_input(
            "Size:", value=1.0, min_value=0.0, key="COMP_SIZE_{}".format(i)
        )
compartment_list = [comp["name"] for comp in compartments]
st.write(" ")
st.markdown("------")

st.markdown("### 2. Define the Drug & Dose")


dosing = st.radio("Dosing:", list(util.dosing_strategies.keys()), horizontal=True)

left, right = st.columns(2)
with left:
    drug_name = st.text_input("Drug Name: ", "Imagiprofen")
    dose_compartment = st.selectbox(
        "Dose Compartment:", compartment_list, placeholder="Choose a compartment"
    )
with right:
    if dosing == "I.V. Infusion":
        drug_dose = st.number_input(
            "Dose:", 0.0, help="Dose Infusion Rate (amount/time)"
        )
    else:
        drug_dose = st.number_input("Dose:", 0.0, help="Dose (amount)")

    dosing_kwargs = dict()
    if dosing == "Oral":
        dosing_kwargs["ka"] = st.number_input(
            "Absorption Rate Constant:",
            0.0,
            help="1st-order rate constant for the absoption.",
        )
        dosing_kwargs["f"] = st.number_input(
            "Bioavailability:", value=1.0, min_value=0.0, max_value=1.0, step=0.01
        )

st.write(" ")
st.markdown("------")

st.markdown("### 3. Drug Distribution")


distributes = []
n_comp = len(compartments)
if n_comp > 1:
    st.write(drug_name, " distribution between compartments:")
    left, center, right = st.columns(3)
    for i in range(n_comp - 1):
        comp_i = compartments[i]["name"]
        for j in range(i + 1, n_comp):
            comp_j = compartments[j]["name"]
            left.write(" ")
            is_on = left.toggle("{} <--> {}".format(comp_i, comp_j))
            if is_on:
                k_dist = center.number_input(
                    "Distribution Rate constant {} --> {}:".format(comp_i, comp_j),
                    0.0,
                    help="1st-order rate constant for the distribution.",
                )
                # center.latex(r"k_f")
                k_redist = right.number_input(
                    "Re-distribution Rate constant {} <-- {}:".format(comp_i, comp_j),
                    0.0,
                    help="1st-order rate constant for the re-distribution.",
                )
                distributes.append([comp_i, comp_j, k_dist, k_redist])
            left.write(" ")
            left.write(" ")
            # left.write(" ")
else:
    st.write("Only one compartment, so no distribution available.")

st.write(" ")
st.markdown("------")

st.markdown("### 4. Drug Elimination")

eliminates = []

st.write(drug_name, " linear elimination from compartments:")

for i in range(n_comp):
    left, center, right = st.columns(3)
    comp_i = compartments[i]["name"]
    # left.write(" ")
    is_on = left.toggle("{}".format(comp_i))
    if is_on:
        k_el = center.number_input(
            "Elimination Rate constant:",
            0.0,
            help="1st-order rate constant for the linear elimination process.",
            key="elimination_rate_{}".format(comp_i),
        )
        # right.markdown("------")
        eliminates.append([comp_i, k_el])
    # left.write(" ")
    # left.write(" ")
    # left.markdown("------")
    # left.write(" ")
    if n_comp > 1:
        st.markdown("------")

# st.write(" ")
# st.markdown("------")

# st.write(distributes)
# st.write(eliminates)
# st.write(compartments)
st.markdown("### 5. Download Your PK Model")
crafted = False
model_text = ""
model_file_name = model_dir + model_name + ".py"


def write_model():
    with open(model_file_name, "w") as f:
        util.built_with(f)
        util.standard_imports(f)
        util.new_model(f)
        util.compartments(f, compartments)
        util.dose(f, drug_name, drug_dose, dose_compartment, dosing, dosing_kwargs)
        if len(distributes) > 0:
            util.distribution(f, drug_name, distributes)
        if len(eliminates) > 0:
            util.elimination(f, drug_name, eliminates)
    crafted = True
    with open(model_file_name, "r") as f:
        model_text = f.read()
    return crafted, model_text


def import_model():
    
    try:
        file_path = ".model/model.py"
        module_name = "model"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        #return sys.modules[module_name]['model']
        return module.model
    except Exception as e:
        st.exception(e)
    return


# left, right = st.columns(2)
# if left.button("Generate the Model"):
#     crafted, model_text = write_model()
#     st.code(model_text, line_numbers=True)
#     right.download_button(
#         "Download the model source code",
#         model_text,
#         model_file_name,
#     )

crafted, model_text = write_model()
if "model_str" in st.session_state:
    if st.session_state.model_str != model_text:
        util.save_model_str(model_text)
        util.reload_saved_model()
        model = st.session_state.model
else:
    model = import_model()
    util.save_model(model)
st.write(model)
st.code(model_text, line_numbers=True)
st.download_button(
    'Download "model.py"',
    model_text,
    model_file_name,
    on_click=st.balloons,
)

st.write(" ")
st.write(" ")
powered_by = "Model powered by PySB {} and pysb-pkpd {}".format(
    version("pysb"), version("pysb.pkpd")
)
st.caption(powered_by)
# st.write(crafted, model_text)
# if left.button("Craft it!"):
#     crafted = write_model()

# if crafted:


# st.write(model_text)


# editor_on = st.toggle("Turn on Code Editor")
# if editor_on:
#     with open(model_file_name, "r") as f:
#         model_text = f.read()
#     from streamlit_monaco import st_monaco
#     content = st_monaco(value=model_text, height="600px", language="python")