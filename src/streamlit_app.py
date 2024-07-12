import streamlit as st
import os
import tempfile


st.logo(
    "https://drive.google.com/thumbnail?id=1VD8GOQyppZDRRqw1p03Akpo_P7fAxsye",
    link=None,
    icon_image="https://drive.google.com/thumbnail?id=1itHVJ4zoncjGCnEWMMjpgyFrz2J6_YP8",
)

if "tmp_dir" not in st.session_state:
    tmp_dir = tempfile.TemporaryDirectory(prefix="aurorpkpd-", delete=False)
    st.session_state.tmp_dir = tmp_dir
    model_file_name = os.path.join(st.session_state.tmp_dir.name, "model.py")
    st.session_state.model_file = model_file_name

home_page = st.Page("home.py", title="Home", icon=":material/house:")
upload_page = st.Page("upload.py", title="Upload", icon=":material/upload:")
build_page = st.Page("build.py", title="Build", icon=":material/build:")
viz_page = st.Page("visualize.py", title="Visualize", icon=":material/hub:")
simulate_page = st.Page("simulate.py", title="🔜Simulate", icon=":material/laps:")
fit_page = st.Page("fit.py", title="🔜Fit/Train", icon=":material/model_training:")
nca_page = st.Page("nca.py", title="🔜NCA", icon=":material/query_stats:")
support_info_page = st.Page(
    "support/info.py", title="Info", icon=":material/info:"
)
# support_help_page = st.Page(
#     "support/help.py", title="Help", icon=":material/help:"
# )

pg = st.navigation(
    {
        " ": [home_page],
        "Compartmental": [upload_page, build_page, viz_page, simulate_page, fit_page],
        "Non-compartmental" : [nca_page],
        "Support": [support_info_page],
    }
)
st.set_page_config(page_title="Aurora PK/PD", page_icon=":sparkles:")
pg.run()
