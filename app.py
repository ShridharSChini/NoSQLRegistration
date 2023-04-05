import streamlit as st
from multiapp import MultiApp
from apps import home, data # import your app modules here

st.set_page_config(layout="wide")
app = MultiApp()

st.markdown("""
# Student Registration

""")

# Add all your application here
app.add_app("Registration Form", home.app)
app.add_app("Database", data.app)
# The main app
app.run()