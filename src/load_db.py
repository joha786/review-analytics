import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///reviews.db")

df = pd.read_csv("data/clean.csv", parse_dates=["date"])
df.to_sql("reviews", engine, if_exists="replace", index=False)

print("Loaded", len(df), "rows into reviews.db")