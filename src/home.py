import streamlit as st
from pathlib import Path
import os
from io import StringIO

st.write(
    "Welcome to Aurora PK/PD, a web app for building, exploring, and fitting compartmental PK/PD models."
)

model_dir = "./.model/"
model_file = model_dir + "model.py"

if os.path.exists(model_dir):
    if os.path.exists(model_file):
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
else:  
    Path(model_dir).mkdir(exist_ok=False)