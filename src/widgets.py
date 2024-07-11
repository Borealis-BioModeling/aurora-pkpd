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
