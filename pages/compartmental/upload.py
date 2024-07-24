import streamlit as st
from pathlib import Path
import os
from io import StringIO
import tempfile
import requests
from app_util import util, widgets

st.title("Upload Your Model")
# st.info("version 0.1.0-alpha")
st.divider()
st.write(
    """
Welcome to the Upload page! Here, you can upload your existing
pharmacokinetic/pharmacodynamic (PK/PD) models in the PySB format.
Aurora PK/PD supports PySB Python files, including the pysb-pkpd and pysb-units add-ons. 
Start a new analysis with an existing model or continue a previous session
with a model constructed using Aurora PK/PD.
"""
)

st.write(" ")
st.markdown("### Would you like to upload an existing PK/PD model?")

if "tmp_dir" not in st.session_state:
    tmp_dir = tempfile.TemporaryDirectory(prefix="aurorpkpd-", delete=False)
    st.session_state.tmp_dir = tmp_dir
    model_file_name = os.path.join(st.session_state.tmp_dir.name, "model.py")
    st.session_state.model_file = model_file_name


left, right = st.columns(2)
# if left.button("Build new model"):
#     st.switch_page("build.py")

left.markdown("### Upload from file:")
uploaded_model = left.file_uploader(" ", type=["py"])

#col1,col2,col3 = st.columns([2,1,1])

if uploaded_model is not None:
    if "model" in st.session_state:
        st.warning(
            "A model has been uploaded or built already. If you save the new model the other one will be overwritten.",
            icon="⚠️",
        )
        model_old = st.session_state.model
        model_text_old = st.session_state.model_str
        st.write("Previously saved model:")
        st.write(model_old)
        st.code(model_text_old, line_numbers=True)
        if st.button("Upload and Overwrite"):
            # To convert to a string based IO:
            stringio = StringIO(uploaded_model.getvalue().decode("utf-8"))
            string_data = stringio.read()
            st.write("Uploaded model:")
            st.code(string_data, line_numbers=True)
            util.save_model_str(string_data)
            with open(st.session_state.model_file, "w") as f:
                f.write(string_data)
            model = util.import_model()
            util.save_model(model)
            widgets.viz_simulate_fit()
            widgets.also_edit()

    else:
        # To convert to a string based IO:
        stringio = StringIO(uploaded_model.getvalue().decode("utf-8"))
        string_data = stringio.read()
        st.write("Uploaded model:")
        st.code(string_data, line_numbers=True)
        util.save_model_str(string_data)
        with open(st.session_state.model_file, "w") as f:
            f.write(string_data)
        model = util.import_model()
        util.save_model(model)
        widgets.viz_simulate_fit()
        widgets.also_edit()
with right:
    st.markdown("### OR,  Load from public repository:")
    repo_host = st.radio("Choose Host", ['GitHub 🐙', 'GitLab 🦊'], horizontal=True)
    
    if repo_host == 'GitHub 🐙':
        repo_user = st.text_input("Username or Organizaton:", placeholder='janedoe')
    elif repo_host == 'GitLab 🦊':
        repo_user = st.text_input("Username or Group:", placeholder='janedoe')
    repo_name = st.text_input("Repository name:", placeholder='my-cool-repo')
    repo_path = st.text_input("Path to model file:", placeholder='src/model.py')
    to_load = st.button("Load")
    with st.expander(":information_source: Sample Model"):
        st.markdown('''
                     If you just want to test things out a bit you can load a sample two-compartment model from the Aurora PK/PD GitHub repo:
                      * Organization: Borealis-BioModeling
                      * Repository name: aurora-pkpd
                      * Path: example_model/twocomp_emax.py
                    ''')
    if to_load:
        if repo_host == 'GitHub 🐙':
            repo_url = f'https://raw.githubusercontent.com/{repo_user}/{repo_name}/main/{repo_path}'
        elif repo_host == 'GitLab 🦊':
            repo_url = f'https://gitlab.com/{repo_user}/{repo_name}/-/raw/master/{repo_path}?ref_type=heads'
        page = requests.get(repo_url)
        string_data = page.text

        util.save_model_str(string_data)
        with open(st.session_state.model_file, "w") as f:
            f.write(string_data)
        model = util.import_model()
        util.save_model(model)
if to_load:
    st.write("Uploaded model:")
    st.code(string_data, line_numbers=True)
    
st.divider()
st.markdown("### Or would you like to build a new custom PK/PD model?")
if st.button("Build new model"):
    st.switch_page("build.py")

from importlib.metadata import version

st.write(" ")
st.write(" ")
powered_by = "Models powered by PySB {} with add-ons: pysb-pkpd {} and pysb-units {}".format(
    version("pysb"), version("pysb.pkpd"), version("pysb.units"),
)
st.caption(powered_by)
