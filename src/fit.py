import streamlit as st
import widgets

st.title("Fit/Train Your Model")

widgets.divider_blank()
st.write(
'''
Welcome to the Fit/Train page! Here, you can upload your concentration-time
profiles and train your pharmacokinetic/pharmacodynamic (PK/PD) model
to fit the data, calibrating your model to your experimental/clinical observations. 
Use this feature to enhance your models predictive capabilities and estimate 
PK parameters for processes like distribution and elimination.
'''
)

widgets.divider_blank()
st.error(
'''
The Fit/Train feature is still under development, including the creation
of another PySB add-on and its integration
into this web app. To accelerate its completion, I’m seeking your support.

Please consider contributing to my fundraising goal to implement this
and other Aurora PK/PD features. Every contribution helps cover my time as an
independent developer and helps get me closer to delivering a more robust set of
open-source tools for PK/PD modeling and analysis.
'''
)
st.link_button(":dollar: Support this Goal on Ko-fi", "https://ko-fi.com/blakeaw/goal?g=0", help="Click to see my Ko-fi page and learn more about this funding Goal.")
