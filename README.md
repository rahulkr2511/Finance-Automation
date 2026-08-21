# SBI Finance Automation

![Status](https://img.shields.io/badge/status-active-brightgreen)

An interactive Streamlit web app for analyzing SBI bank statements — upload
a statement, auto-categorize transactions by keyword matching, and explore
spending through interactive charts, with support for adding your own
custom categories.

## What it does

- Upload a formatted SBI bank statement (CSV) and view transactions in an
  interactive table.
- Auto-categorize transactions using keyword matching against a
  customizable category list.
- Add new categories and keywords on the fly — updates are written to
  `categories.json` in real time via `session_state`.
- Visualize spending by category with interactive pie charts (Plotly).

## Stack

| Purpose | Tech |
|---|---|
| Web app / UI | [Streamlit](https://streamlit.io) — turns the Python script into an interactive dashboard, with `session_state` used to keep category edits in sync live |
| Data manipulation | Pandas |
| Charts | Plotly Express |
| Category storage | JSON (`categories.json`), read/written via `os` and `json` |

## Getting Started

Requires **Python 3** and the dependencies in `requirements.txt`.

```bash
# create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run the app
streamlit run main.py
```

## Preparing your bank statement

SBI exports statements in a format that needs a bit of cleanup before
uploading:

1. Download your bank statement in `.xls` format from SBI.
2. Remove the unnecessary rows from the top and bottom, keeping only the
   transaction rows.
3. Make sure the row with column headers is formatted as the header row,
   then export the file as CSV.
4. Upload the CSV into the app to analyze and categorize.

A `sample_bank_statement.csv` is included in the repo so you can try the
app without needing a real statement.

## Custom categories

`categories.json` stores each category as a key, with a list of keywords
used to match transactions against it.

- `save_category` — adds a new custom category.
- `add_keyword` — updates a category's keyword list when new terms need to
  be recognized.
- Categorized transactions are grouped and visualized as a pie chart.

## Regenerating requirements.txt

```bash
pip install pipreqs
pipreqs . --force

# for any dependency pipreqs misses, get the installed version manually:
pip freeze | grep <dependency-name>   # e.g. pip freeze | grep pandas
```
