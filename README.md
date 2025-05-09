# SBI FinanceAutomation
## It is created using streamlit
    Streamlit is an open-source Python library used to quickly and easily build interactive web applications for data science and machine learning projects — all using pure Python.
    Key Uses of Streamlit:
        Create Interactive Dashboards
            Turn Python scripts into shareable web apps with widgets (like sliders, dropdowns, buttons) that control data and model parameters in real-time.
        Visualize Data Effortlessly
            Use simple commands to display charts, tables, metrics, and images. It supports libraries like Pandas, Matplotlib, Plotly, Altair, and more.
        Deploy Machine Learning Models
            Showcase your ML models with input widgets and display predictions or analytics dynamically — no need for frontend or web dev experience.
        Rapid Prototyping
            Great for fast prototyping of tools, reports, or visual experiments without setting up a full web framework like Flask or Django.
        Interactive Reports
            Ideal for turning Jupyter Notebook insights into beautiful, interactive web reports.
    
    session state property in streamlit is used to update the state dynamically

## Run the application using
    start virtual enviroment using source .venv/bin/activate
    streamlit run main.py

## Pandas is used for data manipulation
## OS and JSON is used for loading json file and writing to it in realtime
## plotly.express is used to display figures and charts

## Steps to analyze the sbi bank statement
    1. download bank statement in xls format
    2. remove all unnecessary rows from top and bottom and keep only the transactions
    3. format the row starts describing all the headers as header and export the file as csv
    4. upload the file in this application and analyze and make changes
