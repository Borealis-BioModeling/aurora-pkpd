
import streamlit as st
util = st.session_state.util_module
widgets = st.session_state.widgets_module

st.title("Support Info")
widgets.divider_blank()





st.markdown("### Have a question or need help with something?")
st.link_button(":question: Ask a question", "https://github.com/Borealis-BioModeling/aurora-pkpd/discussions/new?category=q-a", help="New Q&A Discussion")

widgets.divider_blank()

st.markdown("### Have an idea for a new feature?")
st.link_button(":bulb: Share ideas", "https://github.com/Borealis-BioModeling/aurora-pkpd/discussions/new?category=ideas", help="New Idea Discussion")

st.write(" ")
st.markdown("**OR**")
st.write(" ")

st.markdown("### Want to go ahead and request a new feature?")

st.link_button(":wrench: Submit a feature request", "https://github.com/Borealis-BioModeling/aurora-pkpd/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=", help="New Feature Request")
widgets.divider_blank()

st.markdown("### Found a bug?")
st.markdown("You can help me make this software better by reporting any bugs or other problems using the Issue tracker available through this code's GitHub repository.")
st.link_button(":ladybug: File a bug report", "https://github.com/Borealis-BioModeling/aurora-pkpd/issues/new?assignees=&labels=&projects=&template=bug_report.md&title=", help="Bug Report")
widgets.divider_blank()
#https://github.com/Borealis-BioModeling/aurora-pkpd/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=

st.markdown("### Something else?")
st.link_button(":speech_balloon: Start a new discussion/chat", "https://github.com/Borealis-BioModeling/aurora-pkpd/discussions/new?category=general", help="General Discussions")
widgets.divider_blank()
