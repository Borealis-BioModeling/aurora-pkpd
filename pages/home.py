import streamlit as st
from pathlib import Path
import os
from io import StringIO
import tempfile

util = st.session_state.util_module
widgets = st.session_state.widgets_module

left, center, right = st.columns(3)
center.image(
    "https://drive.google.com/thumbnail?id=1itHVJ4zoncjGCnEWMMjpgyFrz2J6_YP8&sz=w200"
)


# st.title("Aurora PK/PD")
center.info("version 0.1.0-alpha")
widgets.divider_blank()
st.subheader("Aurora PK/PD: Open-Source PK/PD Modeling and Analysis Tools for Academics and Small Startups.")
st.markdown(
    """
Welcome to **Aurora PK/PD**, an open-source Python web app
that aims to provide a robust and accessible set of dynamic
compartmental pharmacokinetics and pharmacodynamics (PK/PD)
modeling and Non-compartmental PK analysis (NCA) tools geared towards
academic researchers and small biotech/pharma startups.

While I haven't completed all the planned features yet, I am
hopeful that Aurora PK/PD will eventually become an essential part
of your model-informed drug discovery and development toolkit that helps
accelerate your efforts to derive pharmacological insights from your clinical data
and ultimately discover new medicines.


Your feedback and support are invaluable in helping Aurora PK/PD grow and evolve.
If you find the software useful, consider contributing to its development,
sharing it with your network, or becoming a financial sponsor to aid its continued
improvement.
"""
)



widgets.divider_blank()
widgets.compartmental_options()
widgets.also_edit()

widgets.divider_blank()
widgets.nca_options()

widgets.divider_blank()

from importlib.metadata import version

st.write(" ")
st.write(" ")
powered_by = "App powered by streamlit {}".format(
    version("streamlit"),
)
st.caption(powered_by)
