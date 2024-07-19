import streamlit as st
from pathlib import Path
import os
from io import StringIO
import tempfile



def load_util_module(module_name: str):
    import importlib.util
    file_path = os.path.join(os.path.dirname(__file__), os.path.relpath("../util/"+module_name+".py"))
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if "tmp_dir" not in st.session_state:
    tmp_dir = tempfile.TemporaryDirectory(prefix="aurorpkpd-")
    st.session_state.tmp_dir = tmp_dir
    model_file_name = os.path.join(st.session_state.tmp_dir.name, "model.py")
    st.session_state.model_file = model_file_name

if "widgets_module" not in st.session_state:
    st.session_state.widgets_module = load_util_module("widgets")

if "util_module" not in st.session_state:
    st.session_state.util_module = load_util_module("util")

util = st.session_state.util_module
widgets = st.session_state.widgets_module



left, center, right = st.columns(3)
center.image(
    "assets/aurora-pkpd-logo-2.png"
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
