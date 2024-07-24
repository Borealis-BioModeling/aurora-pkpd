import streamlit as st
from pathlib import Path
import os
from io import StringIO
import tempfile

from app_util import util, widgets

if "tmp_dir" not in st.session_state:
    tmp_dir = tempfile.TemporaryDirectory(prefix="aurorpkpd-")
    st.session_state.tmp_dir = tmp_dir
    model_file_name = os.path.join(st.session_state.tmp_dir.name, "model.py")
    st.session_state.model_file = model_file_name


left, center, right = st.columns(3)
center.image(
    "assets/aurora-pkpd-logo-2.png"
)

center.info("version 0.1.0-alpha")
widgets.divider_blank()
st.subheader("Aurora PK/PD: Open Web App for Pharmcological Modeling and Analysis")
st.markdown(
    """
Welcome to Aurora PK/PD, an open-source Python web app designed
to provide robust and accessible pharmacokinetics and pharmacodynamics
modeling and analysis tools for academic researchers and small biotech/pharma startups.
I hope Aurora PK/PD can become an essential part of your model-informed drug discovery
and development toolkit, helping you to accelerate your efforts to derive pharmacological
insights from your clinical data and ultimately discover new medicines.

While not all planned features are complete, I hope you 
find the implemented ones useful. Your feedback and support are
invaluable in helping Aurora PK/PD grow and evolve. 
Please visit the *Support Info* page for different ways to share your feedback and ideas
on how to make improve the Aurora PK/PD app:
"""
)
st.page_link(
    "pages/support/info.py", label="Support Info", icon=":material/info:"
)


widgets.divider_blank()
widgets.compartmental_options()
widgets.also_edit()

widgets.divider_blank()
widgets.nca_options()

widgets.divider_blank()
widgets.pdanalysis_options()

from importlib.metadata import version

st.write(" ")
st.write(" ")
powered_by = "App powered by streamlit {}".format(
    version("streamlit"),
)
st.caption(powered_by)
