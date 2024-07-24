import streamlit as st

from app_util import util, widgets

st.title("Analyze High-Througput Cell Proliferation Data")
widgets.divider_blank()
# st.write(
#     """
# This tool lets you fit your experimental data with pharmacodynamic (PD) exposure-response models.
# This feature allows you to analyze how different drugs affect biological systems by fitting
# exposure-response data and other relevant parameters to established PD models. Use this tool to gain
# insights into the efficacy and potency of your compounds and optimize your drug development process.
# """
# )
widgets.divider_blank()
# widgets.under_construction()

st.error(
    """
The HT Cell Proliferation Data analysis feature
is still under development. 
"""
)
widgets.dev_status_planning(issue_number=4)
