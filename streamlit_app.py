import streamlit as st
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Aurora PK/PD", page_icon=":sparkles:")


# --- PAGE SETUP ---
home_page = st.Page("pages/home.py", title="Home", icon=":material/house:")
upload_page = st.Page("pages/compartmental/upload.py", title="Upload", icon=":material/upload:")
build_page = st.Page("pages/compartmental/build.py", title="Build", icon=":material/build:")
edit_page = st.Page("pages/compartmental/edit.py", title="Edit", icon=":material/code:")
viz_page = st.Page("pages/compartmental/visualize.py", title="Visualize", icon=":material/hub:")
simulate_page = st.Page("pages/compartmental/simulate.py", title="🔜Simulate", icon=":material/laps:")
fit_page = st.Page("pages/compartmental/fit.py", title="🔜Fit/Train", icon=":material/model_training:")
analyze_page = st.Page("pages/compartmental/analyze.py", title="🔜Analyze", icon=":material/analytics:")
nca_page = st.Page("pages/noncompartmental/nca.py", title="🔜NCA", icon=":material/query_stats:")
pdfit_page = st.Page("pages/pdanalysis/responsefit.py", title="🔜Exposure-Response", icon=":material/elevation:")
support_info_page = st.Page("pages/support/info.py", title="Info", icon=":material/info:")


# --- NAVIGATION SETUP [WITH SECTIONS]---
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

# --- SHARED ON ALL PAGES ---
st.logo(
    "assets/aurora-pkpd-logo-wide.png",
    link=None,
    icon_image="assets/aurora-pkpd-logo-2.png",
)
st.sidebar.markdown(" A Streamlit web app by [@blakeaw](https://github.com/blakeaw)")
st.sidebar.link_button(":dollar: Sponsor on Ko-fi", "https://ko-fi.com/blakeaw/goal?g=0", help="Click to see my Ko-fi page.")
# --- RUN NAVIGATION ---
pg.run()

