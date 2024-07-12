import streamlit as st
from pathlib import Path
import os
from io import StringIO
import tempfile
import util
import widgets

st.title("Upload Model")
#st.info("version 0.1.0-alpha")
st.divider()
st.write(" ")
st.markdown(
    "### Would you like to upload an existing PK/PD model?"
)

if "tmp_dir" not in st.session_state:
    tmp_dir = tempfile.TemporaryDirectory(prefix="aurorpkpd-", delete=False)
    st.session_state.tmp_dir = tmp_dir
    model_file_name = os.path.join(st.session_state.tmp_dir.name, "model.py")
    st.session_state.model_file = model_file_name


#left, right = st.columns(2)
# if left.button("Build new model"):
#     st.switch_page("build.py")
uploaded_model = st.file_uploader(" ", type=['py'])
if uploaded_model is not None:
    if "model" in st.session_state:
        st.warning('A model has been uploaded or built already. If you save the new model the other one will be overwritten.', icon="⚠️")
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

st.divider()
st.markdown("### Or would you like to build a new custom PK/PD model?")
if st.button("Build new model"):
    st.switch_page("build.py")

from importlib.metadata import version
st.write(" ")
st.write(" ")
powered_by = "Models powered by PySB {} and pysb-pkpd {}".format(
    version("pysb"), version("pysb.pkpd")
)
st.caption(powered_by)
        