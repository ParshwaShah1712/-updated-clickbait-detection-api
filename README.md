# Clickbait Detection API

This project is a Flask-based API that detects malicious clickbait headlines using machine learning.

## Setup Instructions

### Prerequisites
- Python 3.x

### Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip3 install -r requirements.txt
   ```

### Running the Application

1. Navigate to the 'working model' directory:
   ```
   cd "working model"
   ```

2. Run the Flask application:
   ```
   python3 app.py
   ```

3. Access the application in your browser at: http://127.0.0.1:5000

## Project Structure

- `working model/app.py`: Main Flask application
- `working model/train_model.py`: Script to train the machine learning model
- `working model/model.pkl`: Trained machine learning model
- `working model/vectorizer.pkl`: TF-IDF vectorizer for text processing
- `working model/headline_dataset.csv`: Dataset used for training
- `working model/templates/index.html`: Frontend HTML template
- `working model/static/`: Static files (CSS, JavaScript)

## Usage

Enter a headline in the web interface or send a POST request to the `/predict` endpoint with a JSON payload containing a "headline" field.

Example API request:
```json
{
  "headline": "This amazing discovery will change your life forever"
}
```

The API will respond with a prediction indicating whether the headline is "Malicious" or "Safe".

## Chrome Extension (Manifest V3)

This repo includes a `chrome_extension/` folder with a working MV3 extension that:

- Extracts clickable element texts from the active page (buttons, anchors, inputs)
- Sends them as JSON to the Flask endpoint `/predict_batch`
- Injects a floating side panel showing labels and classifications

### Files
- `chrome_extension/manifest.json`
- `chrome_extension/background.js`
- `chrome_extension/content_script.js`
- `chrome_extension/popup.html`
- `chrome_extension/popup.js`
- `chrome_extension/icons/` (add `icon16.png`, `icon48.png`, `icon128.png`)

### Backend CORS

`working model/app.py` enables CORS for localhost and MV3:

```python
from flask_cors import CORS
CORS(app, origins=["http://127.0.0.1:5000", "http://localhost:5000", "chrome-extension://*"])
```

### Run backend

```
cd "working model"
./venv/Scripts/python.exe app.py
```

### Load extension in Chrome
1. Go to `chrome://extensions`
2. Enable Developer mode
3. Click "Load unpacked" and select `chrome_extension/`

### Test workflow
1. Ensure Flask is running at `http://127.0.0.1:5000`
2. Visit any page with buttons
3. Click the extension icon → "Scan Page"
4. A floating panel appears with each label → Safe/Malicious

Notes
- Only button texts are sent to the API (no full HTML)
- API endpoint is configurable in the popup; default is `http://127.0.0.1:5000/predict_batch`