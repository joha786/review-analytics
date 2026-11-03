import pandas as pd
import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Review Analytics", layout="wide")
st.title("Review Analytics Dashboard")
st.caption("Sentiment insights from 50,000 Amazon food reviews")


@st.cache_data(ttl=300)
def get_trend():
    r = requests.get(f"{API_URL}/sentiment-trend", timeout=10)
    r.raise_for_status()
    return pd.DataFrame(r.json())


@st.cache_data(ttl=300)
def get_top_products(limit):
    r = requests.get(f"{API_URL}/top-products", params={"limit": limit}, timeout=10)
    r.raise_for_status()
    return pd.DataFrame(r.json())


try:
    trend = get_trend()
except requests.exceptions.RequestException:
    st.error("Cannot reach the API. Start it with: python -m uvicorn src.api:app --reload")
    st.stop()

# Sidebar filter
trend["year"] = trend["month"].str[:4]
years = sorted(trend["year"].unique())
selected = st.sidebar.multiselect("Years", years, default=years)
trend = trend[trend["year"].isin(selected)]

# Key numbers
totals = trend.groupby("sentiment")["total"].sum()
all_reviews = int(totals.sum())
c1, c2, c3 = st.columns(3)
c1.metric("Reviews", f"{all_reviews:,}")
c2.metric("Positive", f"{totals.get('positive', 0) / all_reviews:.1%}")
c3.metric("Negative", f"{totals.get('negative', 0) / all_reviews:.1%}")

# Charts
left, right = st.columns(2)

with left:
    st.subheader("Reviews per month by sentiment")
    pivot = trend.pivot_table(index="month", columns="sentiment",
                              values="total", aggfunc="sum").fillna(0)
    st.line_chart(pivot)

with right:
    st.subheader("Negative review share per month (%)")
    share = pivot.div(pivot.sum(axis=1), axis=0) * 100
    if "negative" in share:
        st.line_chart(share[["negative"]])

# Top products
st.subheader("Most reviewed products")
limit = st.slider("How many products", 5, 30, 10)
st.dataframe(get_top_products(limit), use_container_width=True)

# Live prediction
st.subheader("Try the model")
text = st.text_area("Type a review")
if st.button("Predict sentiment"):
    if not text.strip():
        st.warning("Please type a review first.")
    else:
        r = requests.post(f"{API_URL}/predict", json={"text": text}, timeout=10)
        if r.status_code == 200:
            st.success(f"Sentiment: {r.json()['sentiment']}")
        else:
            st.error(r.json().get("detail", "Something went wrong"))