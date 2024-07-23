import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from inspect import getmembers, isfunction
import pandas as pd
import pharmacodynamic as prm
from app_util import util, widgets


@st.cache_data
def get_functions(module):
    funcs = getmembers(module, isfunction)
    return funcs


prm_functions = get_functions(prm)


# @st.cache_data
def categorize_prm_functions(prm_functions):
    categories = dict()
    for func in prm_functions:
        response_type = func[1].response_type
        if response_type not in categories:
            categories[response_type] = [func[1]]
        else:
            categories[response_type].append(func[1])
    return categories


def prm_functions_by_name(prm_functions):
    byname = dict()
    for func in prm_functions:
        name = func[1].name
        byname[name] = func[1]
    return byname


if "prm_functions_categorized" not in st.session_state:
    prm_functions_categorized = categorize_prm_functions(prm_functions)
    st.session_state.prm_functions_categorized = prm_functions_categorized
    st.session_state.prm_functions_by_name = prm_functions_by_name(prm_functions)
st.title("Fit Your Exposure-Response Data")
widgets.divider_blank()
st.write(
    """
This tool lets you fit your experimental data with pharmacodynamic (PD) exposure-response models.
This feature allows you to analyze how different drugs affect biological systems by fitting
exposure-response data and other relevant parameters to established PD models. Use this tool to gain
insights into the efficacy and potency of your compounds and optimize your drug development process.
"""
)
widgets.divider_blank()

st.markdown("### 1. Upload Data")



st.markdown("#### Upload File")
data_file = st.file_uploader("___", type=["csv", "xls", "xlsx"])
if data_file is not None:
    extension = data_file.name.split(".")[-1]
    if extension == 'csv':
        st.session_state.er_data = pd.read_csv(data_file)
    else:
        st.session_state.er_data = pd.read_excel(data_file)

st.markdown("### OR")

gsheet_df = widgets.google_sheet_loader()
if gsheet_df is not None:
    st.session_state.er_data = gsheet_df
with st.expander("Try it out with some Sample Data"):
    st.write("You can try out the analysis using the sample data at this link:")
    st.write("https://docs.google.com/spreadsheets/d/1vaynurld-DiuVW97XQlGunyhYqJdOD-CnoxjZveGP1c/edit?usp=sharing")

st.divider()

st.markdown("### 2. View Data")
left, right = st.columns(2)
if "er_data" in st.session_state:
    data_df = st.session_state.er_data
    data_col = data_df.columns
    left.write("Tabular")
    left.dataframe(data_df, hide_index=True)
    right.write("Plot")
    x_col = right.selectbox("Exposure (x-axis)", data_col, index=0)
    y_col = right.multiselect("Response (y-axis)", data_col)
    error_cols = [col for col in data_col if col not in y_col]
    y_err = right.multiselect("Error (y-axis)", error_cols)
    if (len(y_col) > 0):
        if len(y_err) == len(y_col):
            # Using a longform dataframe to plot scatter 
            # with data that has multiple error columns was adapted from
            # https://community.plotly.com/t/setting-multiple-error-bars-with-new-plotly-express-wide-data-feature/40382/9
            long_df = data_df.melt(id_vars=x_col, value_vars=y_col, value_name="Response(s)", var_name="y_name")
            long_df["y_error"] = data_df[y_err].unstack().values
            fig = px.scatter(long_df, x=x_col, y="Response(s)", log_x=True, error_y='y_error', color="y_name")
            #fig.add_trace(go.Line(long_df, x=x_col, y="Response(s)", log_x=True, line='dash'))
        else:
        #right.scatter_chart(data_df, x=x_col, y=y_col)
            fig = px.scatter(data_df, x=x_col, y=y_col, log_x=True)
        right.plotly_chart(fig)
else:
    st.warning("Upload data first!")
st.divider()
st.markdown("### 3. Select the Response Model")
left, right = st.columns(2)

with left:
    response_type = st.selectbox(
        "A. Response Type",
        list(st.session_state.prm_functions_categorized.keys()),
        index=1,
    )

with right:
    response_options = [
        func.name for func in st.session_state.prm_functions_categorized[response_type]
    ]
    response_function_name = st.selectbox(
        "B. Response Function",
        response_options,
        index=len(response_options) - 1,
    )
    response_function = st.session_state.prm_functions_by_name[response_function_name]
    st.latex(response_function.eq_latex)

# st.write(prm_functions_categorized)
# for func in prm_functions:
#     st.write(func[1].name, func[1].response_type)
#     st.latex(func[1].eq_latex)
from importlib.metadata import version
st.write(" ")
st.write(" ")
powered_by = "Exposure-Response analysis powered by pharmacodynamic-response-models {} and plotly {}".format(
    version("pharmacodynamic"), version("plotly")
)
st.caption(powered_by)
