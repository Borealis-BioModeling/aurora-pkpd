import streamlit as st
from pathlib import Path
import os
from io import StringIO
import tempfile
import util
import widgets

left, center, right = st.columns(3)
center.image("https://drive.google.com/thumbnail?id=1itHVJ4zoncjGCnEWMMjpgyFrz2J6_YP8&sz=w200"
)

#st.title("Aurora PK/PD")
center.info("version 0.1.0-alpha")
widgets.divider_blank()
st.write(
    "Welcome to Aurora PK/PD - a Python web app for compartmental PK/PD modeling and Non-compartmental PK analysis (NCA)."
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
