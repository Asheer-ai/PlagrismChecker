# Plagiarism Detection Project

## Overview

This project is a **Plagiarism Detection System** built using **Flask** (for the backend) and **React** (for the frontend). The system allows users to upload text or files to check for plagiarism using AI-driven detection and comparison algorithms. Additionally, users can compare two files for similarity.

## Features

- **AI-Driven Plagiarism Detection**: Utilizes an AI model to check for AI-generated or plagiarized content.
- **Text and File Input**: Allows users to either paste text or upload files for plagiarism detection.
- **File Comparison**: Upload two files to compare their similarity.
- **Detailed Results**: Provides similarity scores with varying levels of plagiarism detection, from "No plagiarism detected" to "Plagiarism detected."

## Technologies Used

### Backend:
- **Flask**: A lightweight Python web framework used to handle API requests.
- **Scikit-learn**: Used for calculating similarity scores using TF-IDF and cosine similarity.
- **NLTK**: Used for text preprocessing, including stopword removal.

### Frontend:
- **React**: A JavaScript library for building the user interface.
- **CSS**: For styling the user interface.

## Project Structure

```bash
PlagiarismChecker/
│
├── Backend/
│   ├── app.py                 # Main Flask application
│   ├── ai_detection_model.py   # Custom AI detection model
│   ├── requirements.txt        # List of dependencies
│   └── ...
│
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GetStarted.js   # Main React component for plagiarism check
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   ├── package.json            # List of dependencies for React
│   └── ...
│
└── README.md                   # Project documentation
```
## Screenshots

![App Screenshot](https://github.com/Asheer-ai/PlagrismChecker/blob/5055aa1f593535cef815adfab4c3148193499d61/Screenshot%202024-09-21%20010623.png)

![App Screenshot](https://github.com/Asheer-ai/PlagrismChecker/blob/f905e79ae7ff0c2aa0c261243295bc7905ee82dd/Screenshot%202024-09-21%20010534.png)

![App Screenshot](https://github.com/Asheer-ai/PlagrismChecker/blob/18ba1a86c2fd877fc41adeaedf5dbc9a12561c11/Screenshot%202024-09-21%20004939.png)

![App Screenshot](https://github.com/Asheer-ai/PlagrismChecker/blob/cf062b7f3e44cb2f19ee2a82aed8c2b7c55de4f0/Screenshot%202024-09-21%20010515.png)
