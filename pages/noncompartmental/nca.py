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
into this web app. 
'''
)

widgets.dev_status_planning(issue_number=3)