import streamlit as st

# col1, col2, col3 = st.columns(3)
# with col2:
    # st.header("Model Explorer")

st.title("Network Visualizer")


if "model" in st.session_state:
    model = st.session_state.model
else:
    st.warning("Need to buil or upload a model first!")
    st.stop()

st.divider()

from pyvipr.pysb_viz.static_viz import PysbStaticViz
import streamlit.components.v1 as components
from pyvis.network import Network
import util

model_viz = PysbStaticViz(model, generate_eqs=True)
#
if len(model.compartments) > 0:
    graph_json = model_viz.sp_comp_view()
else:
    graph_json = model_viz.sp_view()

#left, right = st.columns(2)
#st.write(graph_json)
#st.stop()
#graph_json = model_viz.sp_view()      
# graph_nx = to_networkx(graph_json)
graph_nx = util.to_networkx_compartments(graph_json)
graph_pyvis = Network("250px", "500px", notebook=True, heading="", directed=True)
graph_pyvis.from_nx(graph_nx)
# graph_pyvis.show_buttons(filter_=['physics'])
graph_pyvis.show("comp-view.html")

graph_html = open("comp-view.html", "r", encoding="utf-8")
graph_source = graph_html.read()

#with left:
st.markdown("### 1. Compartment View")
components.html(graph_source, height=250, width=500)

st.divider()

graph_nx = util.to_networkx_species(graph_json)
graph_pyvis = Network("500px", "500px", notebook=True, heading="", directed=True)
graph_pyvis.from_nx(graph_nx)
# graph_pyvis.show_buttons(filter_=['physics'])
graph_pyvis.show("sp-view.html")

graph_html = open("sp-view.html", "r", encoding="utf-8")
graph_source = graph_html.read()

#with right:
st.markdown("### 2. Species View")
components.html(graph_source, height=500, width=500)

from importlib.metadata import version
st.write(" ")
st.write(" ")
powered_by = "Network visualizer powered by PyViPR {} and PyVis {}".format(
    version("pyvipr"), version("pyvis")
)
st.caption(powered_by)