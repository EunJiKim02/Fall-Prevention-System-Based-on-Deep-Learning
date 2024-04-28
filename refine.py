import pandas as pd

path = "data/output.csv"
df = pd.read_csv(path)

# Count the number of -1 in each row
df["minus_ones_count"] = df.apply(lambda row: (row == -1).sum(), axis=1)

# Group by 'Img' and keep the row with the lesser count of -1
df_result = df.sort_values(by="minus_ones_count").drop_duplicates(
    subset="Img", keep="first"
)

# Drop the auxiliary count column
df_result.drop(columns=["minus_ones_count"], inplace=True)
df_result = df_result.sort_values(by="Img")


df_result.to_csv("data/output_refined.csv", index=False)
