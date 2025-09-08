import pandas as pd
import re
import pickle
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def clean_text(text):
    """Lowercase and remove URLs and non-letter characters.

    This mirrors the runtime cleaning in app.py so the
    vectorizer receives identically processed text at train and serve time.
    """
    text = str(text).lower()
    return re.sub(r"http\S+|www\S+|[^a-zA-Z\s]", "", text)


# Load dataset and apply the same cleaning used at inference time
dataset = pd.read_csv("headline_dataset.csv")
dataset["cleaned"] = dataset["headline"].apply(clean_text)


# Build a representation suitable for very short button texts:
# - Word n-grams capture short phrases like "download now" or "free access"
# - Character n-grams are robust to slight spelling/casing variations
word_vectorizer = TfidfVectorizer(
    ngram_range=(1, 3),
    max_features=20000,
    sublinear_tf=True,
)

char_vectorizer = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(3, 5),
    max_features=30000,
    sublinear_tf=True,
)

combined_vectorizer = FeatureUnion([
    ("word", word_vectorizer),
    ("char", char_vectorizer),
])

X = combined_vectorizer.fit_transform(dataset["cleaned"])  # sparse matrix
y = dataset["label"].astype(int).values


# Class-weighted logistic regression to handle any slight label imbalance
model = LogisticRegression(
    class_weight="balanced",
    C=2.0,
    max_iter=1000,
    solver="liblinear",
    n_jobs=None,
)
model.fit(X, y)


# Persist artifacts expected by the Flask app
with open("model.pkl", "wb") as f_model:
    pickle.dump(model, f_model)

with open("vectorizer.pkl", "wb") as f_vec:
    pickle.dump(combined_vectorizer, f_vec)
