import streamlit as st
from app_util import util, widgets

# col1, col2, col3 = st.columns(3)
# with col2:
    # st.header("Model Explorer")

st.title("Visualize The Network of Interactions In Your Model")
st.header("View interactive network visualizations of model compartments and model species.")
widgets.divider_blank()
page_description = '''
Welcome to the Visualize page! Here, you can explore interactive network
visualizations of your pharmacokinetic/pharmacodynamic (PK/PD) model
compartments and species. Use this feature to gain deeper insights, identify key components,
as well as better understand any complex interactions and relationships within your model.
'''
widgets.about_page(page_description)

widgets.divider_blank()

if "model" in st.session_state:
    model = st.session_state.model
else:
    st.warning("Need to build or upload a model first!")
    st.stop()


from pyvipr.pysb_viz.static_viz import PysbStaticViz
import streamlit.components.v1 as components
from pyvis.network import Network

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
if len(model.compartments) > 0:
    graph_nx = util.to_networkx_compartments(graph_json)
else:
    graph_nx = util.to_networkx_species(graph_json)
graph_pyvis = Network("500px", "700px", notebook=True, heading="", directed=True)
graph_pyvis.from_nx(graph_nx)
# graph_pyvis.show_buttons(filter_=['physics'])
graph_pyvis.show("comp-view.html")

graph_html = open("comp-view.html", "r", encoding="utf-8")
graph_source = graph_html.read()

#with left:
st.markdown("### 1. Compartment View")
st.markdown("Highlights the distribution of drug or other species across the different model compartments:")
components.html(graph_source, height=500, width=700)

st.divider()
# if len(model.compartments) > 0:
graph_nx = util.to_networkx_species(graph_json)
# else:
#     graph_nx = util.to_networkx(graph_json)

graph_pyvis = Network("700px", "700px", notebook=True, heading="", directed=True)
graph_pyvis.from_nx(graph_nx)
# graph_pyvis.show_buttons(filter_=['physics'])
graph_pyvis.show("sp-view.html")

graph_html = open("sp-view.html", "r", encoding="utf-8")
graph_source = graph_html.read()

#with right:
st.markdown("### 2. Species View")
st.markdown("Highlights the network of interactions amongst the model species and their different states and locations:")
components.html(graph_source, height=700, width=700)

widgets.blank_divider_blank()
widgets.simulate_fit()
widgets.divider_blank()

from importlib.metadata import version
st.write(" ")
st.write(" ")
powered_by = "Network visualizer powered by PyViPR {} and PyVis {}".format(
    version("pyvipr"), version("pyvis")
)
st.caption(powered_by)