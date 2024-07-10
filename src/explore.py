import streamlit as st

# col1, col2, col3 = st.columns(3)
# with col2:
    # st.header("Model Explorer")

st.title("Model Explorer")

st.info('Not yet implemented', icon="ℹ️")

if "model" in st.session_state:
    model = st.session_state.model
else:
    st.warning("Need to build or upload a model first!")
    st.stop()

