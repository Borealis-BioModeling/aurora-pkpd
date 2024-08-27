import streamlit as st

from app_util import util, widgets

st.title("Analyze Drug Combination Synergy")
widgets.divider_blank()
st.info(
    """
MuSyC is an algorithm for quantifying drug effect synergy. It distinguishes synergy of efficacy from synergy of potency.

The MuSyC web app allows you upload your own data to produce fit parameters and examine dose-response surfaces. It is free for non-commercial use.
"""
)
st.link_button(
 label="💊+💊 Click Here to vist the MuSyC Web App",
 url="https://musyc.lolab.xyz/accounts/login/?next=/",
)
st.caption(
    """
Wooten, D.J., Meyer, C.T., Lubbock, A.L.R. et al. MuSyC is a consensus framework that unifies multi-drug synergy metrics for combinatorial drug discovery. Nat Commun 12, 4607 (2021). https://doi.org/10.1038/s41467-021-24789-z
    """
)