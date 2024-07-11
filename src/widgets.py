import streamlit as st


def viz_simulate_fit():
    st.markdown("### Next you can:")
    left, center, right = st.columns(3)
    left.page_link("visualize.py", label="Visualize Model", icon=":material/hub:")
    center.page_link("simulate.py", label="Simulate Model", icon=":material/laps:")
    right.page_link("fit.py", label="Fit/Train Model", icon=":material/model_training:")


def divider_blank():
    st.divider()
    st.write(" ")


def blank_divider_blank():
    st.write(" ")
    divider_blank()


def under_construction():
    st.warning(
        "Under construction: This section is currently under development. Please check back later.",
        icon="👷‍♂️",
    )

def compartmental_options():
    
    st.markdown("### Compartmental PK/PD modeling")
    st.markdown("#### First - Upload or Build a Model:")
    left, right = st.columns(2)
    left.page_link("upload.py", label="Upload Model", icon=":material/upload:")
    right.page_link("build.py", label="Build Model", icon=":material/build:")
    viz_simulate_fit()

def nca_options():
    st.markdown("### Non-compartmental PK analysis (NCA)")
    st.markdown("#### Run NCA:")
    st.page_link("nca.py", label="NCA", icon=":material/query_stats:")