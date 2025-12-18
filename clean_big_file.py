import pandas as pd

INPUT_FILE = "DLD_TRANSACTIONS_OPEN.csv"
OUTPUT_FILE = "DLD_CLEAN_BIG.csv"

chunksize = 200_000  # safe for most laptops
first_chunk = True

numeric_cols = [
    "procedure_area",
    "actual_worth",
    "meter_sale_price",
    "rent_value",
    "meter_rent_price"
]

for chunk in pd.read_csv(INPUT_FILE, engine="python", sep=None, chunksize=chunksize):
    # Clean numeric columns
    for col in numeric_cols:
        if col in chunk.columns:
            chunk[col] = (
                chunk[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("null", "", regex=False)
                .str.strip()
            )
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

    # Fix date
    chunk["instance_date"] = pd.to_datetime(
        chunk["instance_date"], errors="coerce", dayfirst=True
    )

    # Create Amount
    chunk["Amount"] = chunk["actual_worth"]

    mask_sale = (
        chunk["Amount"].isna() &
        chunk["procedure_area"].notna() &
        chunk["meter_sale_price"].notna()
    )
    chunk.loc[mask_sale, "Amount"] = (
        chunk["procedure_area"] * chunk["meter_sale_price"]
    )

    mask_rent = chunk["Amount"].isna() & chunk["rent_value"].notna()
    chunk.loc[mask_rent, "Amount"] = chunk["rent_value"]

    # Drop invalid rows
    chunk = chunk.dropna(subset=["Amount", "instance_date"])

    # Write to output
    chunk.to_csv(
        OUTPUT_FILE,
        mode="w" if first_chunk else "a",
        index=False,
        header=first_chunk
    )

    first_chunk = False
    print("Processed chunk...")

print("DONE. Clean file saved as:", OUTPUT_FILE)
