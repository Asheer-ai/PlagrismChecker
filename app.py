from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS
import pickle
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize NLTK stopwords
nltk.download('stopwords')

from ai_detection_model import AIDetectionModel

app = Flask(__name__, static_folder='../Frontend/dist', template_folder='../Frontend/dist')
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for simplicity; adjust as needed

# Load AI detection model
try:
    with open("ai_detection_model.pkl", 'rb') as ai_model_file:
        ai_detection_model = pickle.load(ai_model_file)
except FileNotFoundError:
    raise Exception("AI detection model file not found. Please ensure ai_detection_model.pkl exists.")

# Preprocessing functions
def preprocess_text(text):
    # Remove punctuation and numbers
    text = re.sub(r'\W+', ' ', text)
    # Convert to lowercase
    text = text.lower()
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

def get_tfidf_vectors(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return tfidf_matrix

def calculate_similarity(tfidf_matrix):
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]

def is_plagiarized(similarity_score):
    if similarity_score == 0:
        return "No Plagiarism detected"  
    elif 0 < similarity_score < 1:
        return "Plagiarism detected to some extent"  
    else:
        return " plagiarism detected"  

def plagiarism_detector(text1, text2):
    processed_text1 = preprocess_text(text1)
    processed_text2 = preprocess_text(text2)
    
    tfidf_matrix = get_tfidf_vectors(processed_text1, processed_text2)
    similarity_score = calculate_similarity(tfidf_matrix)
    
    plagiarized = is_plagiarized(similarity_score)
    
    return plagiarized, similarity_score

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
        # Use the preloaded AI detection model
        result = ai_detection_model.detect_ai_text(input_text)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"result": result})

# New endpoint for detecting AI-generated text using AI detection model
@app.route('/detect-ai-text', methods=['POST'])
def detect_ai_text():
    data = request.json
    input_text = data.get('text')

    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    # Use the loaded AI detection model
    try:
        result = ai_detection_model.detect_ai_text(input_text)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"result": result})

# New endpoint for comparing two files for plagiarism
@app.route('/compare-files', methods=['POST'])
def compare_files():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "Two files are required"}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return jsonify({"error": "Both files must have filenames"}), 400

    try:
        # Preprocess both files
        text1 = file1.read().decode('utf-8')
        text2 = file2.read().decode('utf-8')
    except Exception as e:
        return jsonify({"error": f"Error reading files: {str(e)}"}), 500

    try:
        # Compute similarity and determine if plagiarized
        tfidf_matrix = get_tfidf_vectors(preprocess_text(text1), preprocess_text(text2))
        similarity_score = calculate_similarity(tfidf_matrix)
        plagiarism_message = is_plagiarized(similarity_score)
    except Exception as e:
        return jsonify({"error": f"Error processing files: {str(e)}"}), 500

    # Return the result with the plagiarism message
    return jsonify({
        "plagiarism_message": plagiarism_message,  # Descriptive plagiarism message
        "similarity_score": float(similarity_score)  # Serialize the float value
    })
if __name__ == '__main__':
    app.run(debug=True)
