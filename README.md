
# AI Resume Intelligence & Job Matching System

## Project Overview

AI Resume Intelligence is a web-based application that analyzes resumes and matches candidates with suitable job opportunities based on their technical skills.

The application uses NLP techniques, Python, and FastAPI to extract skills, identify missing skills, calculate job match percentages, and recommend relevant jobs.

## Features

- Upload resumes in PDF format.
- Extract text from resumes.
- Preprocess resume text using NLP.
- Automatically identify technical skills.
- Extract required skills from job descriptions.
- Calculate resume-to-job matching percentages.
- Identify matching and missing skills.
- Rank job recommendations.
- Interactive web application using FastAPI.

## Technologies Used

- Python
- FastAPI
- Pandas
- NumPy
- NLTK
- PyMuPDF
- Scikit-learn
- HTML
- CSS
- JavaScript

## Project Structure

```text
AI_Resume_Intelligence/
├── src/
├── dataset/
├── resumes/
├── models/
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python -m uvicorn src.app:app --reload
```

### 4. Open the application

http://127.0.0.1:8000

## Future Improvements

- Semantic resume matching using sentence embeddings.
- AI-powered job recommendations.
- Resume scoring and improvement suggestions.
- Skill gap analysis.
- Integration with real-time job platforms.
