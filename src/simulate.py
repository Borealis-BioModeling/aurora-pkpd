import streamlit as st
import widgets

st.title("Simulate Your Model")
widgets.divider_blank()
st.write(
'''
Welcome to the Simulate page! Here, you can interactively adjust
model parameters and simulate your pharmacokinetic/pharmacodynamic (PK/PD)
model using Aurora PK/PD's intuitive graphical interface, allowing you to explore
different scenarios and view key outputs in real-time. Use this feature to adjust parameters
and test hypotheses in order to gain a deeper understanding of your model's behavior.
'''
)
widgets.divider_blank()

widgets.under_construction()

if "model" in st.session_state:
    model = st.session_state.model
else:
    st.warning("Need to build or upload a model first!")
    st.stop()

