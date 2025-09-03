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