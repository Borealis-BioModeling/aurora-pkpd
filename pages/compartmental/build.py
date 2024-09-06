import streamlit as st
from importlib.metadata import version
import os
import importlib.util
import sys
import tempfile
import astropy.units as u

from app_util import util, widgets


# https://discuss.streamlit.io/t/how-to-set-the-background-color-and-text-color-of-st-header-st-write-etc-and-let-the-text-be-showed-at-the-left-side-of-input-and-select-box/11826
def info(text):
    st.markdown(
        f'<p style="background-color:#D3FFCE;color:#000000;font-size:18px;border-radius:1%;">{text}</p>',
        unsafe_allow_html=True,
    )


def about_step(text):
    with st.expander("About this step.", icon=":material/info:"):
        st.success(text)


compartment_counts = {"one": 1, "two": 2, "three": 3}

# col1, col2, col3 = st.columns(3)
# with col2:
#     st.header("Model Builder")
st.title("Build Your Model")
# with col3:
#     st.image("https://avatars.githubusercontent.com/u/163594810?s=200&v=4", width=100)

page_description = """
Welcome to the Build page! Here, you can create a new compartmental
pharmacokinetic/pharmacodynamic (PK/PD) model using Aurora PK/PD's
graphical, interactive step-by-step interface.
         """
widgets.about_page(page_description)

st.write(" ")
st.markdown("------")

# if "model" in st.session_state:
#     st.warning('A model has been uploaded or built already. If you build a new model the other one will be overwritten.', icon="⚠️")
#     model = st.session_state.model
#     model_text = st.session_state.model_str
#     st.write("Previously saved model:")
#     st.write(model)
#     st.code(model_text, line_numbers=True)

#     if st.button("Build new model"):
#         del st.session_state["model"]
#         st.rerun()
#     else:
#         st.stop()

st.markdown("### 1. Define Core Units")
description_step1 = """
    Set the foundational units for your dynamical PK/PD model,
    including time, concentration, and volume.
    This step ensures consistency and accuracy throughout your
    model-building process. All other model parameters with these
    unit types will be automatically converted to the chosen settings 
    during model execution.
    """
about_step(description_step1)

left, center, right = st.columns(3)
with left:
    unit_time = st.selectbox("Time Unit: ", ["s", "h"])
with center:
    unit_concentration = st.selectbox(
        "Concentration Unit: ",
        [
            "g / L",
            "mg / L",
            "ug / L",
            "mcg / L",
            "ng / L",
            "g / mL",
            "mg / mL",
            "ug / mL",
            "mcg / mL",
            "ng / mL",
        ],
    )
with right:
    unit_volume = st.selectbox("Volume Unit: ", ["L", "mL"])

unit_amount = unit_concentration.split("/")[0]
amount_unit = u.Unit(unit_amount)
# st.write(unit_amount, amount_unit)

widgets.divider_blank()

st.markdown("### 2. Define the Compartments")
description_step2 = """    
Specify the number, names, and volumes of
the compartments to include in your PK/PD model.
This step defines the compartmental structure of your model.
"""
about_step(description_step2)

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
        cols = st.columns(3)
        compartments[i]["name"] = cols[0].text_input("Name:", "CENTRAL")
        compartments[i]["size"] = cols[1].number_input(
            "Volume:", value=1.0, min_value=0.0, key="COMP_SIZE_{}".format(i)
        )
        compartments[i]["unit"] = cols[2].selectbox(
            "Unit",
            ["L", "mL"],
            help="Compartment volume unit.",
            key="COMP_UNIT_{}".format(i),
        )
    else:
        cols = st.columns(3)
        compartments[i]["name"] = cols[0].text_input("Name:", "PERIPHERAL_{}".format(i))
        compartments[i]["size"] = cols[1].number_input(
            "Volume:", value=1.0, min_value=0.0, key="COMP_SIZE_{}".format(i)
        )
        compartments[i]["unit"] = cols[2].selectbox(
            "Unit",
            ["L", "mL"],
            help="Compartment volume unit.",
            key="COMP_UNIT_{}".format(i),
        )
compartment_list = [comp["name"] for comp in compartments]
st.write(" ")
st.markdown("------")

st.markdown("### 3. Define the Drug & Dose")
description_step3 = """    
Define the dosing function (e.g., I.V. Bolus), the drug name,
the dose size, and the target compartment. This step sets
the parameters for how the drug is administered within your PK/PD model.
"""
about_step(description_step3)

dosing = st.radio(
    "Dosing:",
    list(util.dosing_strategies.keys()),
    horizontal=True,
    help="Define a model for how the dose of drug is administered.",
    captions=[
        "Instantaneous bolus dose at time zero.",
        "Zero-order addition of the drug over time.",
        "Linear (first-order) absorption of the drug.",
    ],
)

if dosing == "I.V. Bolus":
    st.latex(
        r"\left[\textrm{Drug}\right]_{\textrm{Compartment},\, t=0} = \textrm{Dose} / V_{\textrm{Compartment}}"
    )
elif dosing == "I.V. Infusion":
    # st.latex(r'\frac{\textrm{d}\left[Drug\right]_{\textrm{Compartment}}}{dt} = \frac{\textrm{Dose}}{V_{\textrm{Compartment}}}')
    st.latex(r"R_{\textrm{infusion}} = \frac{\textrm{Dose}}{V_{\textrm{Compartment}}}")
elif dosing == "Oral":
    # st.latex(r'\frac{\textrm{d}\left[Drug\right]_{\textrm{Compartment}}}{dt} = f \times k_{\textrm{abs}} \times \frac{\textrm{Dose}}{V_{\textrm{Compartment}}}')
    st.latex(
        r"R_{\textrm{absorption}} = f \times k_{\textrm{abs}} \times \frac{\textrm{Dose}}{V_{\textrm{Compartment}}}"
    )
    st.info("$f$ is the bioavailibility and $k_{abs}$ is the absorption rate constant.")

left, center, right = st.columns(3)
with left:
    drug_name = st.text_input("Drug Name: ", "Imagiprofen")
    dose_compartment = st.selectbox(
        "Dose Compartment:", compartment_list, placeholder="Choose a compartment"
    )
with center:
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
            "Bioavailability:",
            value=1.0,
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            help="Fraction of the drug dose that gets absorbed.",
        )
# Placeholder
kabs_unit = None
with right:
    if dosing == "I.V. Infusion":
        dose_unit = st.selectbox(
            "Unit",
            ["g / s", "mg / s", "ug / s", "mcg / s", "ng / s"],
            help="Drug dose unit.",
        )
    else:
        dose_unit = st.selectbox(
            "Unit", ["g", "mg", "ug", "mcg", "ng"], help="Drug dose unit."
        )
    if dosing == "Oral":
        kabs_unit = st.selectbox(
            "Unit", ["1 / s", " 1 / h"], help="Absorption rate constant unit."
        )
# Manually convert the dose amounts and unit since
# pysb-units may not autoconvert these values when using
# mass per liter concentrations.
if dosing == "I.V. Infusion":
    new_unit = u.Unit(amount_unit.to_string() + "/ s")
    drug_dose /= new_unit.to(dose_unit)
    dose_unit = new_unit.to_string()
else:
    new_unit = u.Unit(amount_unit.to_string())
    drug_dose /= new_unit.to(dose_unit)
    dose_unit = new_unit.to_string()

st.write(" ")
st.markdown("------")

st.markdown("### 4. Drug Distribution")
description_step4 = """
Set the distribution of the drug between different
compartments and define the associated rate constants.
This step models how the drug moves through the compartments in your PK/PD model.        
"""
about_step(description_step4)

left, right, *other = st.columns(4)
left.write(" ")
left.write("Distribution: ")
left.write(" ")
right.latex(r"R_{C_1 \to C_2} = k_{C_1 \to C_2} \left[ \textrm{Drug} \right]_{C_1}")
left.write("Re-distribution: ")
right.latex(r"R_{C_2 \to C_1} = k_{C_2 \to C_1} \left[ \textrm{Drug} \right]_{C_2}")
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
            is_on = left.toggle("{} and {}".format(comp_i, comp_j))
            if is_on:
                k_dist = center.number_input(
                    "Distribution Rate constant:",
                    min_value=1e-8,
                    step=1e-8,
                    value=0.1,
                    format="%.2e",
                    help="1st-order rate constant for the distribution: {} ➡️ {}".format(
                        comp_i, comp_j
                    ),
                )
                unit_k_dist = right.selectbox(
                    "Unit Distribution",
                    ["1 / s", " 1 / h"],
                    index=1,
                    help="Distribution rate constant unit.",
                    key="unit_distribution_{}_{}".format(comp_i, comp_j),
                )
                # center.latex(r"k_f")
                k_redist = center.number_input(
                    "Re-distribution Rate constant:",
                    min_value=1e-8,
                    step=1e-8,
                    value=0.1,
                    format="%.2e",
                    help="1st-order rate constant for the re-distribution:  {} ⬅️ {}".format(
                        comp_i, comp_j
                    ),
                )
                unit_k_redist = right.selectbox(
                    "Unit Re-distribution\n ",
                    ["1 / s", " 1 / h"],
                    index=1,
                    help="Re-distribution rate constant unit.",
                    key="unit_redistribution_{}_{}".format(comp_i, comp_j),
                )
                distributes.append(
                    [comp_i, comp_j, k_dist, k_redist, unit_k_dist, unit_k_redist]
                )
            left.write(" ")
            left.write(" ")
            left.write(" ")
            left.write(" ")
            left.write(" ")
            left.write(" ")
            if is_on:
                left.divider()
                center.divider()
                right.divider()
            # left.write(" ")
else:
    st.warning("Only one compartment, so no distribution available.")

st.write(" ")
st.markdown("------")

st.markdown("### 5. Drug Elimination")
description_step5 = """
Specify the linear elimination of the drug from the system.
This step models how the drug is removed from your PK/PD model over time.
"""
about_step(description_step5)

st.latex(r"R_{el} = k_{el} \left[ \textrm{Drug} \right]_{\textrm{Compartment}}")
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
            min_value=1e-8,
            step=1e-8,
            value=1e-1,
            format="%.2e",
            help="1st-order rate constant for the linear elimination process.",
            key="elimination_rate_{}".format(comp_i),
        )
        k_el_unit = right.selectbox(
            "Unit",
            ["1 / s", " 1 / h"],
            index=1,
            help="Elimination rate constant unit.",
            key="unit_kel_{}".format(comp_i),
        )
        # right.markdown("------")
        eliminates.append([comp_i, k_el, k_el_unit])
    # left.write(" ")
    # left.write(" ")
    # left.markdown("------")
    # left.write(" ")
    if n_comp > 1:
        st.markdown("------")

st.write(" ")
st.markdown("------")

st.markdown("### 6. Define a Drug PD Model")
description_step6 = """
Specify whether to include a pharmacodynamic (PD) model for the drug, and if so,
define the PD model and its and parameters. This step models the drug's
effects on the biological system.
"""
about_step(description_step6)

pd_model = None
pd_kwargs = {}
pd_units = {}
if st.toggle("PD model"):
    pd_model = st.radio(
        "Available models:", list(util.PD_MODELS.keys()), horizontal=True
    )
    st.latex(util.PD_MODEL_EQS[pd_model])
    left, center, right = st.columns(3)
    with left:
        # drug_name = st.text_input("Drug Name: ", "Imagiprofen")
        effect_compartment = st.selectbox(
            "Effect Compartment:", compartment_list, placeholder="Choose a compartment"
        )
    with center:
        pd_kwargs = util.PD_MODEL_KWARGS[pd_model](drug_name, effect_compartment)
    with right:
        pd_units = util.PD_MODEL_UNITS[pd_model](drug_name, effect_compartment)

st.write(" ")
st.markdown("------")

st.markdown("### 7. Define Observables")
description_step7 = """
    Specify observables that track the concentration of a
    species within the model, including across different compartments.
    This step helps monitor key variables and outputs in your PK/PD model.
    """
about_step(description_step7)

st.write(
    "Add an observable quantity for ", drug_name, " concentration in compartment(s):"
)

observe = list()
for i in range(n_comp):
    left, right = st.columns(2)
    comp_i = compartments[i]["name"]
    # left.write(" ")
    is_on = left.toggle("{}".format(comp_i), key="toggle_observable_{}".format(comp_i))

    if is_on:
        observe.append([drug_name, comp_i])
        right.success(f"[{drug_name}]_{comp_i}")
    else:
        right.warning(f"[{drug_name}]_{comp_i}")
    if n_comp > 1:
        st.markdown("------")

st.write(" ")
st.markdown("------")
# st.write(distributes)
# st.write(eliminates)
# st.write(compartments)
st.markdown("### 8. Save and Download")
description_step8 = """
    Save your completed PK/PD model and download
    it for future use. This final step ensures that your model
    is accessible across the different compartmental modeling pages and 
    that you can return later and continue your analysis by uploading the Downloaded version
    of your model. You can also review the model's source code if you like.
    """
about_step(description_step8)

if "tmp_dir" not in st.session_state:
    tmp_dir = tempfile.TemporaryDirectory(prefix="aurorpkpd-", delete=False)
    st.session_state.tmp_dir = tmp_dir
    model_file_name = os.path.join(st.session_state.tmp_dir.name, "model.py")
    st.session_state.model_file = model_file_name

crafted = False
model_text = ""


def write_model():
    with open(st.session_state.model_file, "w") as f:
        util.built_with(f)
        util.standard_imports(f)
        util.new_model(f)
        util.simulation_units(f, unit_time, unit_concentration, unit_volume)
        util.compartments(f, compartments)
        util.dose(
            f,
            drug_name,
            drug_dose,
            dose_unit,
            dose_compartment,
            dosing,
            dosing_kwargs,
            kabs_unit,
        )
        if len(distributes) > 0:
            util.distribution(f, drug_name, distributes)
        if len(eliminates) > 0:
            util.elimination(f, drug_name, eliminates)
        if pd_model is not None:
            util.pd_model(
                f, drug_name, pd_model, effect_compartment, pd_kwargs, pd_units
            )
        if len(observe) > 0:
            util.observables(f, observe)
    crafted = True
    os.system("python -m black {}".format(st.session_state.model_file))
    with open(st.session_state.model_file, "r") as f:
        model_text = f.read()
    return crafted, model_text


crafted, model_text = write_model()
# if "model_str" in st.session_state:
#     if st.session_state.model_str != model_text:
#         util.save_model_str(model_text)
#         util.reload_saved_model()
#         model = st.session_state.model
# else:
model = util.import_model()


# st.write(model)
with st.expander("See model code", icon=":material/code:"):
    st.code(model_text, line_numbers=True)
left, right = st.columns(2)
right.download_button(
    'Download "model.py"',
    model_text,
    "model.py",
    on_click=st.balloons,
)
if left.button("Save"):

    if "model" in st.session_state:
        st.warning(
            "A model has been uploaded or built already. If you save the new model the other one will be overwritten.",
            icon="⚠️",
        )
        model_old = st.session_state.model
        model_text_old = st.session_state.model_str
        st.write("Previously saved model:")
        # st.write(model_old)
        with st.expander("See old model code"):
            st.code(model_text_old, line_numbers=True)
        if st.button("Save and Overwrite"):
            util.save_model(model)
            util.save_model_str(model_text)
            st.info("Model saved!", icon="💾")
    else:
        util.save_model(model)
        util.save_model_str(model_text)
        st.info("Model saved!", icon="💾")
if "model" in st.session_state:
    widgets.viz_simulate_fit()
    widgets.also_edit()
st.write(" ")
st.write(" ")
powered_by = (
    "Model powered by PySB {} with add-ons: pysb-pkpd {} and pysb-units {}".format(
        version("pysb"), version("pysb.pkpd"), version("pysb.units")
    )
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
