import streamlit as st

util = st.session_state.util_module
widgets = st.session_state.widgets_module

st.title("Fit Your Response Data")
widgets.divider_blank()
st.write(
    """
This tool lets you fit your experimental data with pharmacodynamic (PD) response models.
This feature allows you to analyze how different drugs affect biological systems by fitting
dose-response data and other relevant parameters to established PD models. Use this tool to gain
insights into the efficacy and potency of your compounds and optimize your drug development process.
"""
)
widgets.divider_blank()
# widgets.under_construction()

st.error(
    """
The PD Response Fitting feature
is still under development. To accelerate its completion, I’m seeking your support.

Please consider contributing to my fundraising goal to implement this
and other Aurora PK/PD features. Every contribution helps cover my time as an
independent developer and helps get me closer to delivering a more robust set of
open-source tools for PK/PD modeling and analysis.
"""
)
st.link_button(
    ":dollar: Support this Goal on Ko-fi",
    "https://ko-fi.com/blakeaw/goal?g=0",
    help="Click to see my Ko-fi page and learn more about this funding Goal.",
)
