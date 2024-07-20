import streamlit as st
from app_util import util, widgets

st.title("Analyze Your Model")
widgets.divider_blank()
st.write(
'''
Welcome to the Analyze page! Here, you can perform detailed
analyses of your pharmacokinetic/pharmacodynamic (PK/PD) model,
including local sensitivity analysis and other dynamical model
assessments. Use this feature to gain valuable insights, identify
critical parameters, and better understand the dynamics of your model.
'''
)
widgets.divider_blank()
st.error(
'''
The Analyzer feature is still under development. 
To accelerate its completion, I’m seeking your support.

Please consider contributing to my fundraising goal to implement this
and other Aurora PK/PD features. Every contribution helps cover my time as an
independent developer and helps get me closer to delivering a more robust set of
open-source tools for PK/PD modeling and analysis.
'''
)
st.link_button(":dollar: Support this Goal on Ko-fi", "https://ko-fi.com/blakeaw/goal?g=0", help="Click to see my Ko-fi page and learn more about this funding Goal.")

if "model" in st.session_state:
    model = st.session_state.model
else:
    st.warning("Need to build or upload a model first!")
    st.stop()