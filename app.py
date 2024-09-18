from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS
import pickle

from ai_detection_model import AIDetectionModel

app = Flask(__name__, static_folder='../Frontend/dist', template_folder='../Frontend/dist')
CORS(app, resources={r"/check-plagiarism": {"origins": "http://127.0.0.1:5000"}})

# Load AI detection model
try:
    with open("ai_detection_model.pkl", 'rb') as ai_model_file:
        ai_detection_model = pickle.load(ai_model_file)
except FileNotFoundError:
    raise Exception("AI detection model file not found. Please ensure ai_detection_model.pkl exists.")

# Serve React App
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_react_app(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files for React (CSS, JS, etc.)
@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory(os.path.join(app.static_folder, 'static'), path)

# Endpoint to check plagiarism using the existing AI model
@app.route('/check-plagiarism', methods=['POST'])
def check_plagiarism():
    data = request.json
    input_text = data.get('text')

    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    try:
        with open("ai_detection_model.pkl", 'rb') as model_file:
            model = pickle.load(model_file)
    except FileNotFoundError:
        return jsonify({"error": "Model file not found"}), 500

    # Use detect_ai_text instead of predict
    result = model.detect_ai_text(input_text)

    return jsonify({"result": result})

# New endpoint for detecting AI-generated text using AI detection model
@app.route('/detect-ai-text', methods=['POST'])
def detect_ai_text():
    data = request.json
    input_text = data.get('text')

    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    # Use the loaded AI detection model
    result = ai_detection_model.detect_ai_text(input_text)

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
