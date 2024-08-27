import streamlit as st

from app_util import util, widgets

st.title("Analyze High-Througput Cell Proliferation Data")
widgets.divider_blank()
st.info(
    """
Thunor is a free software platform for managing, visualizing, and analyzing high throughput cell proliferation data.
"""
)
st.link_button(
 label="⚡ Click Here to vist the Thunor Web App",
 url="https://www.thunor.net/",
)
st.caption(
    """
Alexander L R Lubbock, Leonard A Harris, Vito Quaranta, Darren R Tyson, Carlos F Lopez, Thunor: visualization and analysis of high-throughput dose–response datasets, Nucleic Acids Research, Volume 49, Issue W1, 2 July 2021, Pages W633–W640, https://doi.org/10.1093/nar/gkab424
    """
)
