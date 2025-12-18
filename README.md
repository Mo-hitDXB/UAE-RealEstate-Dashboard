# UAE Real Estate Analytics Dashboard
<img width="865" height="486" alt="image" src="https://github.com/user-attachments/assets/97fe2084-de16-492b-9788-13807bc6947b" />

The dashboard uses official Dubai Land Department (DLD) open transaction data.
For this academic project, a cleaned historical dataset is used to demonstrate business analytics, trend identification, and decision-support capabilities.
The system is designed so that live API integration can be added as future scope.


## Project Overview
This project is an interactive Business Intelligence (BI) dashboard built using **Streamlit** to analyze UAE real estate transactions.  
It provides insights into transaction volume, total value, average prices, and trends across years, areas, and property types.

This dashboard was developed as an **academic business analytics project**.

---

## Data Source
- Original dataset: UAE / Dubai Land Department (DLD) real estate transactions
- Format: CSV
- The dataset includes transaction dates, areas, property types, and transaction values (AED)

---

## Dataset Note (Important)
The original dataset was **very large and not suitable for cloud deployment** due to GitHub and Streamlit Cloud size limits.

For deployment and performance reasons:
- A **reduced dataset (~20,000 records)** was used
- The structure and schema remain identical to the original dataset
- All analytics logic and business insights remain valid

This approach follows **industry best practices** for BI dashboards.

---

## Key Features
- Year, area, and property-type filters
- KPI cards (Total Transactions, Total Value, Average Value)
- Monthly transaction value trend
- Top areas by transaction value
- Export filtered data as CSV

---

## Tech Stack
- Python
- Streamlit
- Pandas
- Plotly

---

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run dashboard.py
