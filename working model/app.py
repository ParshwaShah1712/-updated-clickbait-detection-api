from flask import Flask, request, jsonify, render_template
import pickle
import re

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def clean_text(text):
    text = text.lower()
    return re.sub(r"http\S+|www\S+|[^a-zA-Z\s]", "", text)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if request.is_json:
        data = request.get_json()
        link = data.get("link", "")
    else:
        link = request.form.get("link", "")
    
    # Extract text from link for analysis
    cleaned_text = clean_text(link)
    vectorized = vectorizer.transform([cleaned_text])
    prediction = model.predict(vectorized)[0]
    return jsonify({"result": "Malicious" if prediction == 1 else "Safe"})

if __name__ == "__main__":
    app.run(debug=True)
