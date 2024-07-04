import streamlit as st
from importlib.metadata import version
import writing


compartment_counts = {"one": 1, "two": 2, "three": 3}


col1, col2, col3 = st.columns(3)
with col2:
    st.header("PK Crafter App")
with col3:
    st.image('https://avatars.githubusercontent.com/u/163594810?s=200&v=4', width=100)
st.text(
    "Build and export compartmental PK (pharmacokinetics) models in the PySB format."
)
st.write('Powered by PySB ',version("pysb"), " and pysb-pkpd ", version("pysb.pkpd"))
st.write(" ")
st.markdown("------")

st.header("1. Name The Model")
model_name = st.text_input("Model Name:", "pkmodel")

st.write(" ")
st.markdown("------")

st.header("2. Define the Compartments")

compartments = []
n_comp = 1
#num_compartment = st.radio("Number of Compartments:", ["one", "two", "three", "more"])
#if num_compartment == "more":
n_comp = st.number_input("Number of Compartments:", value=1, min_value=1, step=1)
#else:
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

st.write(" ")
st.markdown("------")

st.header("3. Define the Drug & Dose")

left, right = st.columns(2)


with left:
    drug_name = st.text_input("Drug Name: ", "Imagiprofen")
    drug_dose = st.number_input("Dose:", 0.0)

with right:
    dosing = st.radio("Dosing:", list(writing.dosing_strategies.keys()))
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

st.write(compartments)

crafted = False
if st.button("Craft it!"):
    # pysb.Model()
    # pkpd.two_compartments()
    # drug = pkpd.drug_monomer(drug_name)[0]
    # dosing_strategies[dosing](drug, CENTRAL, drug_dose, **dosing_kwargs)
    # st.write(model)
    # from pysb.export import export
    model_file_name = model_name + ".py"
    with open(model_file_name, 'w') as f:
        writing.standard_imports(f)
    crafted = True    


if crafted:
    with open(model_file_name, 'r') as f:
        model_text = f.read()
    st.write(model_text)
    st.download_button("Download model", model_text, file_name=model_file_name)
