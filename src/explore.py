import pandas as pd

df = pd.read_csv("data/Reviews.csv")
print(df.shape)
print(df.columns.tolist())
print(df.head(3))
print(df["Score"].value_counts())
print(df.isna().sum())