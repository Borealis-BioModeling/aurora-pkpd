import streamlit as st
from pathlib import Path
import os
from io import StringIO
import tempfile
import util
import widgets

left, center, right = st.columns(3)
center.image(
    "https://drive.google.com/thumbnail?id=1itHVJ4zoncjGCnEWMMjpgyFrz2J6_YP8&sz=w200"
)

# st.title("Aurora PK/PD")
center.info("version 0.1.0-alpha")
widgets.divider_blank()
st.subheader("This is Aurora PK/PD")
st.write(
    """
Welcome to Aurora PK/PD, an open-source Python web app
aiming to provide a robust and accessible set of dynamic
compartmental pharmacokinetics and pharmacodynamics (PK/PD)
modeling and Non-compartmental PK analysis (NCA) tools for
academic researchers and small biotech/pharma startups.

While not all features are fully completed yet, I am
hopeful that Aurora PK/PD will become an essential part
of your drug discovery toolkit, enabling you to conserve
critical funds while still gaining the pharmacological insights
 needed to advance your research efforts.

Your feedback and support are invaluable in helping Aurora PK/PD grow and evolve.
If you find the software useful, consider contributing to its development, spreading
the word within the wider community, or becoming a financial sponsor to aid its continued
improvement. Together, we can make an impact on the future of pharmacological modeling
and analysis.
"""
)
# st.write(
#     "Explore Aurora PK/PD, an open-source Python web app designed for dynamic compartmental PK/PD modeling and robust Non-compartmental PK analysis (NCA). Created specifically for academic researchers and small biotech/pharma startups, Aurora PK/PD offers a free suite of high-quality modeling and analysis tools, enabling you to conserve your limited funds while still obtaining the pharmacological insights needed to take your drug discovery efforts to the next level! "
# )


widgets.divider_blank()
widgets.compartmental_options()
widgets.also_edit()

widgets.divider_blank()
widgets.nca_options()

widgets.divider_blank()

from importlib.metadata import version

st.write(" ")
st.write(" ")
powered_by = "App powered by streamlit {}".format(
    version("streamlit"),
)
st.caption(powered_by)
