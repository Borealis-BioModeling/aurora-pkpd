import streamlit as st
from pathlib import Path
import os
from io import StringIO
import tempfile
import util
import widgets

left, center, right = st.columns(3)
center.image(
    "https://drive.google.com/thumbnail?id=1itHVJ4zoncjGCnEWMMjpgyFrz2J6_YP8&sz=w200"
)

# st.title("Aurora PK/PD")
center.info("version 0.1.0-alpha")
widgets.divider_blank()
st.subheader("Introducing Aurora PK/PD")
st.write(
    "Explore Aurora PK/PD, an open-source Python web app designed for dynamic compartmental PK/PD modeling and robust Non-compartmental PK analysis (NCA). Created specifically for academic researchers and small biotech/pharma startups, Aurora PK/PD offers a free suite of high-quality modeling and analysis tools, enabling you to conserve your limited funds while still obtaining the pharmacological insights needed to take your drug discovery efforts to the next level! "
)


widgets.divider_blank()
widgets.compartmental_options()

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
