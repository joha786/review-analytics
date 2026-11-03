import pandas as pd


def label(score):
    if score <= 2:
        return "negative"
    if score == 3:
        return "neutral"
    return "positive"


def clean(df):
    df = df.drop_duplicates(subset=["UserId", "ProfileName", "Time", "Text"])
    df = df.dropna(subset=["Text", "Score"])
    df = df[df["Text"].str.strip() != ""].copy()
    df["date"] = pd.to_datetime(df["Time"], unit="s")
    df["sentiment"] = df["Score"].map(label)
    return df[["Id", "ProductId", "Text", "Score", "date", "sentiment"]]


if __name__ == "__main__":
    df = pd.read_csv("data/Reviews.csv")
    print("Before cleaning:", len(df))

    df = clean(df)
    print("After cleaning:", len(df))

    df = df.sample(50000, random_state=42)
    df.to_csv("data/clean.csv", index=False)
    print("Saved 50,000 rows to data/clean.csv")
    print(df["sentiment"].value_counts())