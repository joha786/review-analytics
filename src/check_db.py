import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///reviews.db")
print(pd.read_sql("SELECT COUNT(*) AS total FROM reviews", engine))
print(pd.read_sql("SELECT * FROM reviews LIMIT 3", engine))