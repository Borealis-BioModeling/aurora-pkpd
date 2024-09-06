import streamlit as st
from app_util import util, widgets

st.title("Fit/Train Your Model")

widgets.divider_blank()
page_description = '''
Welcome to the Fit/Train page! Here, you can upload your concentration-time
profiles and train your pharmacokinetic/pharmacodynamic (PK/PD) model
to fit the data, calibrating your model to your experimental/clinical observations. 
Use this feature to enhance your models predictive capabilities and estimate 
PK parameters for processes like distribution and elimination.
'''
widgets.about_page(page_description)

widgets.divider_blank()
st.error(
'''
The Fit/Train feature is still under development, including the creation
of another PySB add-on and its integration
into this web app.
'''
)

widgets.dev_status_planning(issue_number=7)