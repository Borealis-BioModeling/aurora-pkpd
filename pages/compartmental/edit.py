import streamlit as st
util = st.session_state.util_module
widgets = st.session_state.widgets_module

st.title("Edit Your Model")

widgets.divider_blank()

st.write(
'''
Welcome to the Edit page! Here, you can work
directly with the underlying model code using
our embedded code editor. This feature is designed
for advanced users who need to implement more
sophisticated and customized pharmacokinetic/pharmacodynamic (PK/PD) models.
'''
)
widgets.divider_blank()

if "model" in st.session_state:
    model = st.session_state.model
    model_txt = st.session_state.model_str
else:
    st.warning("Need to build or upload a model first!")
    st.stop()


from streamlit_monaco import st_monaco
content = st_monaco(value=model_txt, height="800px", language="python")

if st.button(":floppy_disk: Save Changes"):
    with open(st.session_state.model_file, "w") as f:
        f.write(content)
    model = util.import_model()
    if model is None:
        st.warning("Unable to import the model due to an error. Save was aborted.", icon="⚠️")
        st.stop()
    util.save_model(model)
    util.save_model_str(content)
    st.rerun()
    # except:
    #     st.warning("")

widgets.viz_simulate_fit()

from importlib.metadata import version

st.write(" ")
st.write(" ")
powered_by = "Editor powered by streamlit-monaco {}".format(
    version("streamlit-monaco"),
)
st.caption(powered_by)
