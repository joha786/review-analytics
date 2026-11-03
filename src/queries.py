import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///reviews.db")

queries = {
    "1. Reviews per sentiment": """
        SELECT sentiment, COUNT(*) AS total
        FROM reviews
        GROUP BY sentiment
        ORDER BY total DESC
    """,
    "2. Average rating per year": """
        SELECT strftime('%Y', date) AS year,
               ROUND(AVG(Score), 2) AS avg_rating,
               COUNT(*) AS total_reviews
        FROM reviews
        GROUP BY year
        ORDER BY year
    """,
    "3. Monthly sentiment trend (latest 36 rows)": """
        SELECT strftime('%Y-%m', date) AS month, sentiment, COUNT(*) AS total
        FROM reviews
        GROUP BY month, sentiment
        ORDER BY month DESC
        LIMIT 36
    """,
    "4. Most reviewed products": """
        SELECT ProductId, COUNT(*) AS total_reviews,
               ROUND(AVG(Score), 2) AS avg_rating
        FROM reviews
        GROUP BY ProductId
        ORDER BY total_reviews DESC
        LIMIT 10
    """,
    "5. Worst-rated products (at least 20 reviews)": """
        SELECT ProductId, COUNT(*) AS total_reviews,
               ROUND(AVG(Score), 2) AS avg_rating
        FROM reviews
        GROUP BY ProductId
        HAVING COUNT(*) >= 20
        ORDER BY avg_rating ASC
        LIMIT 10
    """,
    "6. Percent of negative reviews per year": """
        SELECT strftime('%Y', date) AS year,
               ROUND(100.0 * SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_negative
        FROM reviews
        GROUP BY year
        ORDER BY year
    """,
    "7. Average review length by sentiment": """
        SELECT sentiment, ROUND(AVG(LENGTH(Text)), 0) AS avg_chars
        FROM reviews
        GROUP BY sentiment
    """,
}

for title, sql in queries.items():
    print("\n" + title)
    print(pd.read_sql(sql, engine).to_string(index=False))