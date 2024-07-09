import streamlit as st
from pathlib import Path
import os
from io import StringIO

st.title("Home")
st.write(
    "Welcome to Aurora PK/PD, a web app for building, exploring, and fitting compartmental PK/PD models."
)

if "tmp_dir" not in st.session_state:
    tmp_dir = tempfile.TemporaryDirectory(delete=False)
    st.session_state.tmp_dir = tmp_dir
    model_file_name = os.path.join(st.session_state.tmp_dir.name, "model.py")
    st.session_state.model_file = model_file_name

if "model" in st.session_state:
    st.write("Model exists!")
    st.write(st.session_state.model)
else:
    left, right = st.columns(2)
    if left.button("Build new model"):
        st.switch_page("build.py")
    uploaded_model = right.file_uploader("Upload existing model", type=['py'])
    if uploaded_model is not None:
        # To convert to a string based IO:
        stringio = StringIO(uploaded_model.getvalue().decode("utf-8"))
        string_data = stringio.read()
        st.write("Uploaded model:")
        st.code(string_data, line_numbers=True)
