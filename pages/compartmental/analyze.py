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
'''
)

widgets.dev_status_planning(issue_number=8)