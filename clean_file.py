import pandas as pd

# Load your exact file
df = pd.read_csv("DLD_TRANSACTIONS_OPEN.csv", engine="python", sep=None)

# Columns to clean
numeric_cols = [
    "procedure_area",
    "actual_worth",
    "meter_sale_price",
    "rent_value",
    "meter_rent_price"
]

# CLEAN NUMERIC FIELDS
for col in numeric_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "")
        .str.replace("null", "")
        .str.replace(" ", "")
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# CLEAN DATE FIELD
df["instance_date"] = pd.to_datetime(
    df["instance_date"], errors="coerce", dayfirst=True
)

# CREATE AMOUNT FIELD
df["Amount"] = df["actual_worth"]

mask_sale = (
    df["Amount"].isna() &
    df["procedure_area"].notna() &
    df["meter_sale_price"].notna()
)

df.loc[mask_sale, "Amount"] = (
    df["procedure_area"] * df["meter_sale_price"]
)

mask_rent = (
    df["Amount"].isna() &
    df["rent_value"].notna()
)

df.loc[mask_rent, "Amount"] = df["rent_value"]

# DROP USELESS ROWS
df = df.dropna(subset=["Amount", "instance_date"])

# SAVE CLEAN FILE
df.to_csv("DLD_CLEAN.csv", index=False)

print("Cleaning complete!")
print("Original rows:", 199)
print("Cleaned rows:", df.shape[0])
print("Saved as: DLD_CLEAN.csv")
