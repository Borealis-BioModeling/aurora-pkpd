from copy import deepcopy
import streamlit as st
import numpy as np
import pandas as pd
import pysb.pkpd as pkpd
from pysb.units.core import Model
from app_util import util, widgets
import matplotlib.pyplot as plt


if "sim_traj_df" not in st.session_state:
    st.session_state.sim_traj_df = None

st.title("Simulate Your Model")
widgets.divider_blank()
st.write(
    """
Welcome to the Simulate page! Here, you can interactively adjust
model parameters and simulate your pharmacokinetic/pharmacodynamic (PK/PD)
model using Aurora PK/PD's intuitive graphical interface, allowing you to explore
different scenarios and view key outputs in real-time. Use this feature to adjust parameters
and test hypotheses in order to gain a deeper understanding of your model's behavior.
"""
)
widgets.divider_blank()

widgets.under_construction()

if "model" in st.session_state:
    model = deepcopy(st.session_state.model)
else:
    st.warning("Need to build or upload a model first!")
    st.stop()


nominals = [param.value for param in model.parameters]
param_categories = [
    "dose",
    "compartment_volumes",
    "rate_constants",
    "initial_concentrations",
]
pd_names = ["Emax", "Linear", "LogLinear", "SigmoidalEmax", "FixedEffect"]
# def catagorize_parameters(model):
#     categorized = dict()
#     for item in param_categories:
#         categorized[item] = dict()
#     for compartment in model.compartments:
#         categorized['compartment_volumes'][compartment.name] = compartment.size
#     for rule in model.rules:
#         r_f = rule.rate_forward
#         r_r = rule.rate_reverse
#         categorized['rate_constants'][r_f.name] = r_f
#         if rule.is_reversible:
#             categorized['rate_constants'][r_r.name] = r_r
#     for param in model.parameters:

#     return categorized


def catagorize_parameters(model):
    categorized = dict()
    for compartment in model.compartments:
        categorized[compartment.size.name] = "Compartment Size"
    for rule in model.rules:
        r_f = rule.rate_forward
        r_r = rule.rate_reverse
        categorized[r_f.name] = "Forward Rate Constant"
        if rule.is_reversible:
            categorized[r_r.name] = "Reverse Rate Constant"
    for param in model.parameters:
        if "dose" in param.name:
            categorized[param.name] = "Dose"
        for item in pd_names:
            if item in param.name:
                categorized[param.name] = "PD Parameter"
                break
    for initial in model.initials:
        try:
            name = initial.value.name
            param = initial.value
            value = param.value
            categorized[name] = "Initial Concentration"
        except:
            pass

    return categorized


params_categorized = catagorize_parameters(model)


st.subheader("Model Parameters")
st.divider()
cols = st.columns(3)
col_idx = 0
for param, nominal in zip(model.parameters, nominals):
    if param.name in params_categorized:
        help_str = params_categorized[param.name]
    else:
        help_str = None
    if param.has_units:
        unit = param.units.value
    else:
        unit = None

    # st.write(param.name, unit)
    # min_value = nominal / 1000.0
    # max_value = nominal * 1000.0
    # step = np.logspace(np.log(min_value), np.log(max_value), 200)
    # st.write(step)
    param.value = cols[col_idx].number_input(
        param.name + f" ({unit})",
        # min_value=min_value,
        # max_value=max_value,
        value=nominal,
        # options=step,
        help=help_str,
        # format="%.2e",
    )
    col_idx += 1
    if col_idx == 3:
        col_idx = 0
# st.subheader("Simulate")
time_unit = model.simulation_units.time
time_col = "Time" + f" ({time_unit})"
concentration_unit = model.simulation_units.concentration
st.divider()
left, right = st.columns(2)
with left:
    value = None
    max_value = None
    if time_unit == "s":
        value = 300.0
        max_value = 24.0 * 60.0 * 60.0
    elif time_unit == "h":
        value = 24.0
        max_value = 24.0 * 14.0
    total_time = st.slider(
        "Set Simulation " + time_col,
        value=value,
        min_value=1.0,
        max_value=max_value,
        step=1.0,
    )
    tspan = np.arange(0, total_time + 1)
if right.button("-------------- Run Simulation -----------------"):
    with right:
        with st.spinner("Running..."):
            sim_traj = pkpd.simulate(model, tspan)
            sim_traj_df = pd.DataFrame(sim_traj)
            # Remove the "private" outputs
            cols = [c for c in sim_traj_df.columns if not c.startswith("_")]
            sim_traj_df = sim_traj_df[cols]
            # Add the timespan
            sim_traj_df.insert(0, time_col, tspan)
            st.session_state.sim_traj_df = sim_traj_df
st.divider()
left, center, right = st.columns(3)
with left:

    if st.session_state.sim_traj_df is not None:
        st.write("Trajectory Data")
        st.dataframe(st.session_state.sim_traj_df, hide_index=True)

with center:
    if st.session_state.sim_traj_df is not None:
        sim_traj_df = st.session_state.sim_traj_df

        st.write("Observables")
        st.line_chart(
            data=sim_traj_df,
            x=time_col,
            y=[c for c in sim_traj_df.columns if c.startswith("obs")],
            y_label=concentration_unit,
        )

with right:
    if st.session_state.sim_traj_df is not None:
        sim_traj_df = st.session_state.sim_traj_df
        effect_col = [c for c in sim_traj_df.columns if ("expr" in c)]
        if len(effect_col) > 0:
            st.write("Effects")
            st.line_chart(
                data=sim_traj_df,
                x=time_col,
                y=effect_col,
                y_label="Effect",
            )
