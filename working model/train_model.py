import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

def clean_text(text):
    text = text.lower()
    return re.sub(r"http\S+|www\S+|[^a-zA-Z\s]", "", text)

df = pd.read_csv("headline_dataset.csv")
df["cleaned"] = df["headline"].apply(clean_text)

vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["cleaned"])
y = df["label"]

model = LogisticRegression()
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
