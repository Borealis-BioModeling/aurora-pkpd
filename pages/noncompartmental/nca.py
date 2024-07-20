import streamlit as st
from app_util import util, widgets

st.title("Non-Compartmental Analysis (NCA)")
widgets.divider_blank()
st.write(
'''
Welcome to the NCA page! Here, you can upload your
concentration-time profiles and perform non-compartmental
pharmacokinetic (PK) analysis on the data. Use this feature to
calculate key PK parameters such as Cmax, Tmax, AUC, and half-life, without 
assuming any specific compartmental model.
'''
)
widgets.divider_blank()
#widgets.under_construction()

st.error(
'''
The Non-Compartmental Analysis (NCA) feature
is still under development, including the creation
of a Python-based NCA package and its integration
into this web app. To accelerate its completion, I’m seeking your support.

Please consider contributing to my fundraising goal to implement this
and other Aurora PK/PD features. Every contribution helps cover my time as an
independent developer and helps get me closer to delivering a more robust set of
open-source tools for PK/PD modeling and analysis.
'''
)
st.link_button(":dollar: Support this Goal on Ko-fi", "https://ko-fi.com/blakeaw/goal?g=0", help="Click to see my Ko-fi page and learn more about this funding Goal.")
