import streamlit as st

st.logo(
    "https://avatars.githubusercontent.com/u/163594810?s=200&v=4",
    link="https://github.com/Borealis-BioModeling",
)

home_page = st.Page("home.py", title="Home", icon=":material/home:")
build_page = st.Page("build.py", title="Build", icon=":material/build:")
explore_page = st.Page("explore.py", title="Explore", icon=":material/lab_research:")
fit_page = st.Page("fit.py", title="Fit/Train", icon=":material/model_training:")

pg = st.navigation([home_page, build_page, explore_page, fit_page])
st.set_page_config(page_title="Aurora PK/PD", page_icon=":sparkles:")
pg.run()
