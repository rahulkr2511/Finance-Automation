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

# Function to add a new keyword to a category
def add_keyword(category, keyword):
    keyword = keyword.lower().strip()
    if category and category in st.session_state.categories: 
        if keyword and keyword not in st.session_state.categories[category]:
            st.session_state.categories[category].append(keyword)
            save_categories()
            st.success(f"Keyword '{keyword}' added to category '{category}'")
            return True
        else:
            st.warning(f"Keyword '{keyword}' already exists in category '{category}'")
            return False
    else:
        st.error(f"Category '{category}' does not exist. Please create it first.")
        return False




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

            # Copy the debit and credit transactions to session state
            st.session_state.debit_transactions = df_debit
            st.session_state.credit_transactions = df_credit

            # Create tabs for debit and credit transactions
            tab1, tab2 = st.tabs(["Debit Transactions", "Credit Transactions"])
            with tab1:
                st.subheader("Expenses details")

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
                edited_df = st.data_editor(
                    st.session_state.debit_transactions[["Date", "Details", "Amount", "Category"]], 
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                        "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category", 
                            options=list(st.session_state.categories.keys()), 
                            default="Uncategorized",
                        ),
                    },
                    use_container_width=True,
                    hide_index=True,
                    key="debit_transactions_editor",
                )

                save_button = st.button("Save Changes", type="primary")
                if save_button:
                    for id, row in edited_df.iterrows():
                        new_category = row["Category"]
                        if row["Category"] == st.session_state.debit_transactions.at[id, "Category"]:
                            continue
                        new_keyword = row["Details"]
                        st.session_state.debit_transactions.at[id, "Category"] = new_category
                        add_keyword(new_category, new_keyword)


                    # Save the changes to the session state
                    st.session_state.debit_transactions = edited_df
                    st.success("Changes saved successfully!")
                

                # Create a bar chart for debit transactions
                fig = px.bar(df_debit, x="Date", y="Amount", title="Debit Transactions Over Time")
                st.plotly_chart(fig)

                # Summary statistics
                st.subheader("Summary Statistics")
                category_total = st.session_state.debit_transactions.groupby("Category")["Amount"].sum().reset_index()
                category_total = category_total.sort_values(by="Amount", ascending=False)
                st.write(category_total)

                fig = px.pie(category_total, values="Amount", names="Category", title="Expenses by Category")
                st.plotly_chart(fig, use_container_width=True)

                
            with tab2:  
                st.subheader("Income details")

                # Display total income
                total_income = df_credit["Amount"].sum()    
                st.metric(label="Total Income", value=f"{total_income:,.2f} AED")

                # Display the credit transactions
                st.write(df_credit)
                # Create a bar chart for credit transactions
                fig = px.bar(df_credit, x="Date", y="Amount", title="Credit Transactions Over Time")
                st.plotly_chart(fig)


                

main()

