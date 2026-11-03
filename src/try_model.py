import joblib

model = joblib.load("src/model.joblib")
samples = [
    "Absolutely delicious, I will buy this again!",
    "Terrible taste and it arrived damaged.",
    "It's okay, nothing special.",
]
for s in samples:
    print(model.predict([s])[0], "->", s)