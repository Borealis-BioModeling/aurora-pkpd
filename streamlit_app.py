import streamlit as st
import os
import tempfile

st.set_page_config(page_title="Aurora PK/PD", page_icon=":sparkles:")

st.logo(
    "assets/aurora-pkpd-logo-wide.png",
    link=None,
    icon_image="assets/aurora-pkpd-logo-2.png",
)



def load_util_module(module_name: str):
    import importlib.util
    file_path = os.path.join(os.path.dirname(__file__), os.path.relpath("util/"+module_name+".py"))
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

home_page = st.Page("pages/home.py", title="Home", icon=":material/house:")
upload_page = st.Page("pages/compartmental/upload.py", title="Upload", icon=":material/upload:")
build_page = st.Page("pages/compartmental/build.py", title="Build", icon=":material/build:")
edit_page = st.Page("pages/compartmental/edit.py", title="Edit", icon=":material/code:")
viz_page = st.Page("pages/compartmental/visualize.py", title="Visualize", icon=":material/hub:")
simulate_page = st.Page("pages/compartmental/simulate.py", title="🔜Simulate", icon=":material/laps:")
fit_page = st.Page("pages/compartmental/fit.py", title="🔜Fit/Train", icon=":material/model_training:")
analyze_page = st.Page("pages/compartmental/analyze.py", title="🔜Analyze", icon=":material/analytics:")
nca_page = st.Page("pages/noncompartmental/nca.py", title="🔜NCA", icon=":material/query_stats:")
pdfit_page = st.Page("pages/pdanalysis/responsefit.py", title="🔜Response Fit", icon=":material/elevation:")
support_info_page = st.Page("pages/support/info.py", title="Info", icon=":material/info:")
# support_help_page = st.Page(
#     "support/help.py", title="Help", icon=":material/help:"
# )

pg = st.navigation(
    {
        " ": [home_page],
        "Compartmental PK/PD": [
            upload_page,
            build_page,
            edit_page,
            viz_page,
            simulate_page,
            fit_page,
            analyze_page,
        ],
        "Non-compartmental PK": [nca_page],
        "PD Analysis": [pdfit_page],
        "Support": [support_info_page],
    }
)

pg.run()

