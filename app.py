
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pymupdf
import pandas as pd
import re
import os

app = FastAPI(title="AI Resume Intelligence")


# -----------------------------------------
# Technical Skills
# -----------------------------------------

technical_skills = [
    "python", "sql", "mysql",
    "machine learning", "deep learning",
    "nlp", "fastapi", "flask", "django",
    "pandas", "numpy", "matplotlib",
    "seaborn", "scikit-learn",
    "regression", "classification",
    "random forest", "decision tree",
    "xgboost", "langchain", "langgraph",
    "rag", "faiss", "generative ai",
    "tensorflow", "pytorch",
    "prompt engineering", "github"
]


# -----------------------------------------
# Extract Resume Text
# -----------------------------------------

def extract_resume_text(file_path):

    document = pymupdf.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


# -----------------------------------------
# Extract Skills
# -----------------------------------------

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in technical_skills:

        pattern = r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


# -----------------------------------------
# Job Matching
# -----------------------------------------

def match_jobs(resume_skills):

    file_path = "dataset/jobs_with_extracted_skills.csv"

    if not os.path.exists(file_path):
        return []

    df = pd.read_csv(file_path)

    results = []

    for index, row in df.iterrows():

        job_skills = [
            skill.strip().lower()
            for skill in str(row["extracted_skills"]).split(",")
            if skill.strip()
        ]

        matching_skills = set(resume_skills).intersection(job_skills)

        missing_skills = set(job_skills) - set(resume_skills)

        if len(job_skills) > 0:

            percentage = (
                len(matching_skills) / len(job_skills)
            ) * 100

        else:
            percentage = 0

        results.append({
            "job_title": row["job_title"],
            "company_name": row["company_name"],
            "match_percentage": round(percentage, 2),
            "matching_skills": sorted(matching_skills),
            "missing_skills": sorted(missing_skills)
        })

    results.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return results


# -----------------------------------------
# Home Page
# -----------------------------------------

@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>
    <html>
    <head>

        <title>AI Resume Intelligence</title>

        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: Arial, sans-serif;
                background: #f4f5fb;
                color: #20213a;
            }

            header {
                background: #171b3b;
                color: white;
                padding: 25px 8%;
            }

            header h2 {
                margin-bottom: 8px;
            }

            .hero {
                text-align: center;
                padding: 65px 20px;
                background: linear-gradient(135deg, #24295c, #7656cf);
                color: white;
            }

            .hero h1 {
                font-size: 38px;
                margin-bottom: 15px;
            }

            .hero p {
                font-size: 17px;
            }

            .upload-card {
                background: white;
                width: 85%;
                max-width: 650px;
                margin: 40px auto;
                padding: 35px;
                text-align: center;
                border-radius: 15px;
                box-shadow: 0 5px 20px #00000012;
            }

            .upload-card h2 {
                margin-bottom: 15px;
            }

            input[type="file"] {
                display: block;
                margin: 25px auto;
                max-width: 100%;
            }

            button {
                background: #6250c8;
                color: white;
                padding: 14px 30px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background: #4434a5;
            }

            #status {
                margin-top: 15px;
                color: #6250c8;
            }

            .results {
                width: 85%;
                max-width: 1100px;
                margin: 30px auto;
                display: none;
            }

            .results h2 {
                margin-bottom: 20px;
            }

            .result-card {
                background: white;
                padding: 25px;
                margin-bottom: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 15px #00000010;
            }

            .result-card h3 {
                margin-bottom: 15px;
                color: #493aab;
            }

            .skill {
                display: inline-block;
                background: #e9e5ff;
                color: #4434a5;
                padding: 8px 13px;
                margin: 5px;
                border-radius: 20px;
                font-size: 14px;
            }

            .job {
                border: 1px solid #e4e4ed;
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 10px;
            }

            .job h3 {
                color: #24295c;
                margin-bottom: 10px;
            }

            .match {
                color: #16834a;
                font-weight: bold;
                margin: 12px 0;
            }

            .missing {
                background: #fff0e8;
                color: #b64c20;
            }

            footer {
                text-align: center;
                background: #171b3b;
                color: white;
                padding: 20px;
                margin-top: 50px;
            }

            @media(max-width: 600px) {
                .hero h1 {
                    font-size: 28px;
                }

                .upload-card {
                    width: 92%;
                }
            }

        </style>

    </head>

    <body>

        <header>

            <h2>AI Resume Intelligence</h2>

            <p>Smart Resume Analysis & Job Matching Platform</p>

        </header>


        <section class="hero">

            <h1>Find Your Perfect Job Match</h1>

            <p>
                Upload your resume and discover how well
                your skills match available job opportunities.
            </p>

        </section>


        <section class="upload-card">

            <h2>Upload Your Resume</h2>

            <p>Upload your resume in PDF format</p>

            <input type="file" id="resumeFile" accept=".pdf">

            <button onclick="analyzeResume()">
                Analyze Resume
            </button>

            <p id="status"></p>

        </section>


        <section id="results" class="results">

            <h2>Resume Analysis Results</h2>

            <div class="result-card">

                <h3>Extracted Technical Skills</h3>

                <div id="skills"></div>

            </div>


            <div class="result-card">

                <h3>Recommended Jobs</h3>

                <div id="jobs"></div>

            </div>

        </section>


        <footer>

            <p>AI Resume Intelligence | Powered by Machine Learning</p>

        </footer>


        <script>

            async function analyzeResume() {

                const file = document.getElementById("resumeFile").files[0];

                const status = document.getElementById("status");

                if (!file) {

                    status.innerText = "Please upload your resume first.";

                    return;
                }

                if (!file.name.toLowerCase().endsWith(".pdf")) {

                    status.innerText = "Please upload a PDF file.";

                    return;
                }

                status.innerText = "Analyzing your resume...";

                const formData = new FormData();

                formData.append("file", file);

                try {

                    const response = await fetch("/analyze-resume", {
                        method: "POST",
                        body: formData
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.detail || "Analysis failed");
                    }

                    if (data.error) {
                        throw new Error(data.error);
                    }

                    document.getElementById("results").style.display = "block";

                    const skillsDiv = document.getElementById("skills");

                    skillsDiv.innerHTML = "";

                    data.extracted_skills.forEach(skill => {

                        skillsDiv.innerHTML +=
                            `<span class="skill">${skill}</span>`;

                    });


                    const jobsDiv = document.getElementById("jobs");

                    jobsDiv.innerHTML = "";

                    if (data.job_matches.length === 0) {

                        jobsDiv.innerHTML = "<p>No job matches found.</p>";

                    }

                    data.job_matches.forEach(job => {

                        jobsDiv.innerHTML += `

                            <div class="job">

                                <h3>${job.job_title}</h3>

                                <p>${job.company_name || "Company not specified"}</p>

                                <p class="match">
                                    Match Percentage: ${job.match_percentage}%
                                </p>

                                <p><b>Matching Skills:</b></p>

                                <div>
                                    ${job.matching_skills.map(
                                        skill => `<span class="skill">${skill}</span>`
                                    ).join("")}
                                </div>

                                <p><b>Missing Skills:</b></p>

                                <div>
                                    ${job.missing_skills.map(
                                        skill => `<span class="skill missing">${skill}</span>`
                                    ).join("")}
                                </div>

                            </div>

                        `;

                    });

                    status.innerText = "Resume analysis completed successfully!";

                }

                catch (error) {

                    status.innerText = "Error: " + error.message;

                }

            }

        </script>

    </body>
    </html>
    """


# -----------------------------------------
# Resume Analysis API
# -----------------------------------------

@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF files are supported."}

    os.makedirs("resumes/uploads", exist_ok=True)

    file_path = os.path.join(
        "resumes/uploads",
        os.path.basename(file.filename)
    )

    content = await file.read()

    if not content.startswith(b"%PDF-"):
        return {"error": "Invalid PDF file."}

    with open(file_path, "wb") as output_file:
        output_file.write(content)

    try:

        resume_text = extract_resume_text(file_path)

        if not resume_text.strip():
            return {"error": "No readable text found in this PDF."}

        resume_skills = extract_skills(resume_text)

        job_results = match_jobs(resume_skills)

        return {
            "message": "Resume analyzed successfully",
            "extracted_skills": resume_skills,
            "total_skills": len(resume_skills),
            "job_matches": job_results
        }

    except Exception as error:

        return {"error": str(error)}
