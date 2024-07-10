import streamlit as st
import os
import tempfile

st.logo(
    "https://avatars.githubusercontent.com/u/163594810?s=200&v=4",
    link="https://github.com/Borealis-BioModeling",
)

if "tmp_dir" not in st.session_state:
    tmp_dir = tempfile.TemporaryDirectory(prefix="aurorpkpd-", delete=False)
    st.session_state.tmp_dir = tmp_dir
    model_file_name = os.path.join(st.session_state.tmp_dir.name, "model.py")
    st.session_state.model_file = model_file_name

home_page = st.Page("home.py", title="Home", icon=":material/home:")
build_page = st.Page("build.py", title="Build", icon=":material/build:")
viz_page = st.Page("visualize.py", title="Visualize", icon=":material/hub:")
explore_page = st.Page("explore.py", title="Explore", icon=":material/lab_research:")
fit_page = st.Page("fit.py", title="Fit/Train", icon=":material/model_training:")
support_bug_page = st.Page(
    "support/bugs.py", title="Bugs", icon=":material/bug_report:"
)
support_help_page = st.Page(
    "support/help.py", title="Help", icon=":material/help:"
)

pg = st.navigation(
    {
        " ": [home_page],
        "Tools": [build_page, viz_page, explore_page, fit_page],
        "Support": [support_help_page, support_bug_page],
    }
)
st.set_page_config(page_title="Aurora PK/PD", page_icon=":sparkles:")
pg.run()
