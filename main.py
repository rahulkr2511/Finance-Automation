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


# Create a session state to store the categories
if "categories" not in st.session_state:
    st.session_state.categories = {
        "Uncategorized": []
    }

# Load the categories from a JSON file if it exists
if os.path.exists("categories.json"):
    with open("categories.json", "r") as f:
        st.session_state.categories = json.load(f)
# Function to save categories to a JSON file
def save_categories():
    with open("categories.json", "w") as f:
        json.dump(st.session_state.categories, f)

# Function to categorize transactions
def categorize_transaction(df):
    # Create a new column for the category
    df["Category"] = "Uncategorized"
    # Iterate through the categories and assign them to the transactions
    for category, keywords in st.session_state.categories.items():
        if category == "Uncategorized" or not keywords:
            continue
        keywords_lowercase = [keyword.lower() for keyword in keywords]

        for id, row in df.iterrows():
            details = row["Details"].lower().strip()
            if details in keywords_lowercase:
                df.at[id, "Category"] = category
                break
    return df




# Define the main function and create uploader to upload the CSV file
def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()  # Remove leading/trailing whitespace from column names
        df["Amount"] = df["Amount"].replace({'\$': '', ',': ''}, regex=True).astype(float)
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y", errors="coerce")
        st.write(df)

        # Categorize the transactions and return the updated DataFrame
        return categorize_transaction(df)
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None
def main():
    st.title("Finance Dashboard")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        df = load_transactions(uploaded_file)

        # Separate the debit and credit transactions
        if df is not None:
            df_debit = df[df["Debit/Credit"] == "Debit"].copy()
            df_credit = df[df["Debit/Credit"] == "Credit"].copy()

            # Create tabs for debit and credit transactions
            tab1, tab2 = st.tabs(["Debit Transactions", "Credit Transactions"])
            with tab1:
                st.subheader("Debit Transactions")

                # Add new category input
                new_category = st.text_input("Add a new category")
                if st.button("Add Category"):
                    if new_category:
                        # Add the new category to the session state
                        st.session_state.categories[new_category] = []
                        save_categories()
                        st.rerun()
                    else:
                        st.error("Please enter a category name.")

                # Display the debit transactions
                st.write(df_debit)

                # Create a bar chart for debit transactions
                fig = px.bar(df_debit, x="Date", y="Amount", title="Debit Transactions Over Time")
                st.plotly_chart(fig)
                
            with tab2:  
                st.subheader("Credit Transactions")
                st.write(df_credit)
                # Create a bar chart for credit transactions
                fig = px.bar(df_credit, x="Date", y="Amount", title="Credit Transactions Over Time")
                st.plotly_chart(fig)


                

main()

