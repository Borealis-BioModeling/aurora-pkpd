import streamlit as st
from pathlib import Path
import os
from io import StringIO
import tempfile
import util

st.title("Aurora PK/PD")
st.info("version 0.1.0-alpha")
st.write(
    "Welcome to Aurora PK/PD compartmental PK/PD modeling and Non-compartmental PK analysis (NCA)."
)

from importlib.metadata import version
st.write(" ")
st.write(" ")
powered_by = "App powered by streamlit {}".format(
    version("streamlit"),
)
st.caption(powered_by)