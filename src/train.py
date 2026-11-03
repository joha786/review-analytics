import json
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

df = pd.read_csv("data/clean.csv")

X_train, X_test, y_train, y_test = train_test_split(
    df["Text"],
    df["sentiment"],
    test_size=0.2,
    random_state=42,
    stratify=df["sentiment"],
)
print("Train size:", len(X_train), "| Test size:", len(X_test))

model = make_pipeline(
    TfidfVectorizer(max_features=50000, ngram_range=(1, 2), stop_words="english"),
    LogisticRegression(max_iter=1000, class_weight="balanced"),
)
model.fit(X_train, y_train)

pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
macro_f1 = f1_score(y_test, pred, average="macro")

print(classification_report(y_test, pred))
print("Accuracy:", round(acc, 4))
print("Macro F1:", round(macro_f1, 4))

joblib.dump(model, "src/model.joblib")

with open("src/results.json", "w") as f:
    json.dump({"model": "TF-IDF + Logistic Regression",
               "accuracy": round(acc, 4),
               "macro_f1": round(macro_f1, 4)}, f, indent=2)
print("Saved src/model.joblib and src/results.json")