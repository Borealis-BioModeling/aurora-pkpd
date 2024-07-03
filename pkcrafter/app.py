import streamlit as st
import pysb
import pysb.pkpd as pkpd

dosing_strategies = {"I.V. Bolus": pkpd.dose_bolus, "I.V. Infusion": pkpd.dose_infusion, "Oral": pkpd.dose_absorbed}

st.title("PK Crafter App")

st.write(" ")
st.markdown("------")

model_name = st.text_input("Model Name:", "pkmodel")

st.write(" ")
st.markdown("------")

st.header("Drug")

left, right = st.columns(2)


with left:
    drug_name = st.text_input("Drug Name: ", "Imagiprofen")
    drug_dose = st.number_input("Dose:", 0.)

with right:
    dosing = st.radio("Dosing:", list(dosing_strategies.keys()))
    dosing_kwargs = dict()
    if dosing == 'Oral':
        dosing_kwargs['ka'] = st.number_input("Absorption Rate Constant:", 0., help="1st-order rate constant for the absoption.")
        dosing_kwargs['f'] = st.number_input("Bioavailability:", value=1., min_value=0., max_value=1., step=0.01)

st.write(" ")
st.markdown("------")

if st.button("Craft it:"):
    pysb.Model()
    pkpd.two_compartments()
    drug = pkpd.drug_monomer(drug_name)[0]
    dosing_strategies[dosing](drug, CENTRAL, drug_dose, **dosing_kwargs)
    st.write(model)
    from pysb.export import export
    model_text = export(model, 'pysb_flat')
    st.download_button("Download model", model_text, file_name=model_name+".py")