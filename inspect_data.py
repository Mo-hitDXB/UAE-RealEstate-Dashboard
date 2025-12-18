import pandas as pd

df = pd.read_csv("DLD_TRANSACTIONS_OPEN.csv")

# Show first 20 rows
print("\n------ HEAD 20 ------")
print(df.head(20))

# Show data types
print("\n------ DATA TYPES ------")
print(df.dtypes)

# Show unique values in actual_worth
print("\n------ SAMPLE actual_worth ------")
print(df["actual_worth"].unique()[:30])

# Show unique values in instance_date
print("\n------ SAMPLE instance_date ------")
print(df["instance_date"].unique()[:30])
