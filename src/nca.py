import streamlit as st
import widgets

st.title("Non-Compartmental Analysis (NCA)")
widgets.divider_blank()
st.write(
'''
Welcome to the NCA page! Here, you can upload your
concentration-time profiles and perform non-compartmental
pharmacokinetic (PK) analysis on the data. Use this feature to
calculate key PK parameters such as Cmax, Tmax, AUC, and half-life, without 
assuming any specific compartmental model.
'''
)
widgets.divider_blank()
#widgets.under_construction()

st.error(
'''
This feature is still under development, which includes developing 
a separate Python-based NCA package along with its incorporation here in this
web app. To accelerate it's completion, I'm seeking your support.

Please consider contributing to my fundraising goal of $1000 to 
get this feature implemented. All finanical contributions directly
support the development of this feature, and every contribution helps.
'''
)
st.link_button(":dollar: Sponsor this feature", "https://ko-fi.com/blakeaw/goal?g=0", help="Ko-fi Goal")
