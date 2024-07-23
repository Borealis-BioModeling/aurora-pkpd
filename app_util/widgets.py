import streamlit as st
from app_util import util


def simulate_fit():
    st.markdown("#### Next you can:")
    left, right = st.columns(2)
    left.page_link(
        "pages/compartmental/simulate.py",
        label="Simulate Model",
        icon=":material/laps:",
    )
    right.page_link(
        "pages/compartmental/fit.py",
        label="Fit/Train Model",
        icon=":material/model_training:",
    )


def viz_simulate_fit():
    st.markdown("#### Next you can:")
    left, center, right = st.columns(3)
    left.page_link(
        "pages/compartmental/visualize.py",
        label="Visualize Model",
        icon=":material/hub:",
    )
    center.page_link(
        "pages/compartmental/simulate.py",
        label="Simulate Model",
        icon=":material/laps:",
    )
    right.page_link(
        "pages/compartmental/fit.py",
        label="Fit/Train Model",
        icon=":material/model_training:",
    )


def also_edit():
    # st.markdown("#### You can also:")
    st.page_link(
        "pages/compartmental/edit.py", label="Edit Model Code", icon=":material/code:"
    )


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


def model_check_notification():
    if "model" in st.session_state:
        st.info("NOTE: A model has already been uploaded or built.")


def compartmental_options():

    st.markdown("### Compartmental PK/PD modeling")
    st.markdown("#### First - Upload or Build a Model:")
    left, right = st.columns(2)
    left.page_link(
        "pages/compartmental/upload.py", label="Upload Model", icon=":material/upload:"
    )
    right.page_link(
        "pages/compartmental/build.py", label="Build Model", icon=":material/build:"
    )
    model_check_notification()
    viz_simulate_fit()


def nca_options():
    st.markdown("### Non-compartmental PK analysis (NCA)")
    st.markdown("#### Run NCA:")
    st.page_link(
        "pages/noncompartmental/nca.py", label="NCA", icon=":material/query_stats:"
    )


def google_sheet_loader():
    st.markdown("#### Load Data from Google Sheet")
    sharing_link = st.text_input(
        "Input Sharing Link: ",
        placeholder="https://docs.google.com/spreadsheets/d/SHEET-ID/edit?usp=sharing",
    )
    if st.button("Load Sheet"):
        try:
            df_sheet = util.load_gsheet(sharing_link)

        except:
            if sharing_link is None:
                st.warning("Please provide a sharing link to the Google Sheet.")
                return None
            else:
                st.warning(
                    "Unable to load the sheet. Make sure the link is correct and has the appropriate permissions."
                )
                return None
        return df_sheet
