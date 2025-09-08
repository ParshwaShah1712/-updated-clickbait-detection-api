from flask import Flask, request, jsonify, render_template
import pickle
import re
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
# Allow all origins during development to support chrome-extension:// origin and preflight
CORS(app)
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

@app.route("/predict_batch", methods=["POST"])
def predict_batch():
	# Accepts JSON payload: { "links": ["text1", "text2", ...] }
	if not request.is_json:
		return jsonify({"error": "Expected application/json"}), 400
	payload = request.get_json(silent=True) or {}
	items = payload.get("links", [])
	if not isinstance(items, list):
		return jsonify({"error": "'links' must be a list of strings"}), 400

	cleaned = [clean_text(x or "") for x in items]
	vectorized = vectorizer.transform(cleaned)
	preds = model.predict(vectorized)
	results = ["Malicious" if p == 1 else "Safe" for p in preds]
	return jsonify({"results": results})

def extract_button_texts_from_html(html):
	texts = []
	try:
		soup = BeautifulSoup(html or "", "lxml")
	except Exception:
		# Fallback to built-in parser if lxml not available
		soup = BeautifulSoup(html or "", "html.parser")

	candidates = []
	candidates.extend(soup.find_all(["a", "button"]))
	candidates.extend(soup.select("[role='button']"))
	candidates.extend(soup.select("input[type='submit'], input[type='button']"))

	seen = set()
	for el in candidates:
		text = (el.get_text(strip=True) or el.get("value") or "").strip()
		if not text:
			continue
		if len(text) < 2:
			continue
		if text in seen:
			continue
		seen.add(text)
		texts.append(text)
	return texts

@app.route("/extract_and_predict", methods=["POST"])
def extract_and_predict():
	# Accepts JSON payload: { "html": "<html>..." }
	if not request.is_json:
		return jsonify({"error": "Expected application/json"}), 400
	payload = request.get_json(silent=True) or {}
	html = payload.get("html", "")
	if not html:
		return jsonify({"error": "'html' is required"}), 400

	texts = extract_button_texts_from_html(html)
	if not texts:
		return jsonify({"buttons": [], "results": []})

	cleaned = [clean_text(t) for t in texts]
	vectorized = vectorizer.transform(cleaned)
	preds = model.predict(vectorized)
	results = ["Malicious" if p == 1 else "Safe" for p in preds]
	return jsonify({"buttons": texts, "results": results})

if __name__ == "__main__":
	app.run(debug=True)
