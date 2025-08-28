# Import necessary libraries
import numpy as np
import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Load the dataset
df = pd.read_csv('headlines.csv')  # Replace with your dataset filename

# Preprocessing the data
df.drop_duplicates(inplace=True)  # Remove duplicate rows
df.dropna(inplace=True)  # Remove rows with missing values
df.reset_index(drop=True, inplace=True)  # Reset the index after cleaning

# Initialize TF-IDF vectorizer and preprocess text data
vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(df['headline'].values.astype('U'))  # Transform headlines into numerical features
y = df['label']  # Labels: 1 for malicious, 0 for benign

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")

# Save the model and vectorizer for deployment
joblib.dump(model, 'model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
