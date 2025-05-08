import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
import os


# Setting up the page configuration
# Set the page title and icon
# Set the layout to wide
st.set_page_config(page_title="Finance Automation", page_icon=":money_with_wings:", layout="wide")


# Define the main function and create uploader to upload the CSV file

def load_transactions(file):
    pass

def main():
    st.title("Finance Dashboard")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
    

main()

