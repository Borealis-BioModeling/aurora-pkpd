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


center.info("version 0.3.0-alpha")
widgets.divider_blank()
st.subheader("Aurora PK/PD: Open Web App for Pharmacological Modeling and Analysis")
st.markdown(
    """
Welcome to Aurora PK/PD! This open-source Python web app aims to provide 
a versatile and accessible pharmacokinetics
and pharmacodynamics modeling and analysis platform that is particularly
suited to rapid prototyping and exploratory analysis. I hope Aurora PK/PD will offer students, academic researchers, and small biotech/pharma startups
a cost-effective alternative to proprietary PK/PD software, making it easier to learn,
explore, and accelerate drug discovery. 

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

widgets.blank_divider_blank()
st.subheader("What would you like to do?")
left, center, right = st.columns(3)

with left:
    with st.expander("Compartmental Modeling", icon=":material/widgets:"):
        widgets.compartmental_options()
        widgets.also_edit()

with center:
    with st.expander("Non-compartmental Analysis", icon=":material/query_stats:"):
        widgets.nca_options()

with right:
    with st.expander("Pharmacodynamic Analysis", icon=":material/bid_landscape:"):
        widgets.pdanalysis_options()

from importlib.metadata import version

st.write(" ")
st.write(" ")
powered_by = "App powered by streamlit {}".format(
    version("streamlit"),
)
st.caption(powered_by)
