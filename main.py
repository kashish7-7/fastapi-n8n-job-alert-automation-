from fastapi import FastAPI, UploadFile, File
import pdfplumber
import re
import io
import requests

app = FastAPI()

# ================== N8N WEBHOOK (TEST URL) ==================
# IMPORTANT:
# Use webhook-test URL while clicking "Execute workflow" in n8n
# Switch to /webhook/ (production) ONLY after activating workflow

N8N_WEBHOOK_URL = "https://kash6397764096y4974945545.app.n8n.cloud/webhook-test/resume-ingest"

# ================== SKILLS DATABASE ==================

TECH_SKILLS = {
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "go", "rust", "php", "ruby", "r", "matlab", "kotlin", "swift",
    "fastapi", "django", "flask", "spring", "spring boot",
    "react", "angular", "vue", "node.js", "express",
    "html", "css", "bootstrap", "tailwind",
    "mysql", "postgresql", "mongodb", "sqlite", "oracle", "redis",
    "numpy", "pandas", "scikit-learn", "tensorflow", "pytorch",
    "machine learning", "deep learning", "nlp",
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
    "ci/cd", "terraform",
    "git", "github", "gitlab", "jira", "postman", "linux"
}

# ================== PDF TEXT EXTRACTION ==================

def extract_text_from_pdf(file):
    text = ""
    try:
        pdf_file = io.BytesIO(file.read())
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        return ""
    return text

# ================== SKILL EXTRACTION ==================

def extract_skills(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z0-9+.# ]', ' ', text)

    found = set()
    for skill in TECH_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.add(skill)

    return sorted(found)

# ================== EDUCATION EXTRACTION ==================

def extract_education(text):
    text = text.lower()
    if re.search(r'\b(ph\.?d|doctorate)\b', text):
        return "PhD"
    if re.search(r'\b(mba|m\.?tech|m\.?sc|master\s+of|masters?)\b', text):
        return "Master's"
    if re.search(r'\b(b\.?tech|b\.?e|b\.?sc|bachelor|undergraduate)\b', text):
        return "Bachelor's"
    if re.search(r'\b(diploma|polytechnic)\b', text):
        return "Diploma"
    if re.search(r'\b(12th|hsc|higher\s+secondary)\b', text):
        return "12th Grade"
    if re.search(r'\b(10th|sslc|secondary)\b', text):
        return "10th Grade"
    return "Not Mentioned"

# ================== EXPERIENCE EXTRACTION ==================

def extract_experience(text):
    text = text.lower()
    years = re.findall(r'(\d+)\s*\+?\s*years?', text)
    if years:
        y = max(map(int, years))
        if y >= 10:
            return "Senior (10+ years)"
        if y >= 5:
            return "Mid-Level (5–9 years)"
        if y >= 2:
            return "Junior (2–4 years)"
        return "Entry-Level (1 year)"
    if re.search(r'\b(fresher|intern|internship|graduate)\b', text):
        return "Fresher"
    return "Fresher"

# ================== MAIN API ENDPOINT ==================

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    text = extract_text_from_pdf(file.file)
    if not text:
        return {"error": "Could not extract text from PDF"}

    # Build final result
    result = {
        "skills": extract_skills(text),
        "education_level": extract_education(text),
        "experience_level": extract_experience(text)
    }

    # Send REAL extracted data to n8n webhook
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=result,
            timeout=5
        )
        print("Webhook sent → status:", response.status_code)
    except Exception as e:
        print("Failed to send to n8n:", e)

    # Return response to user
    return result

# ================== ROOT ==================

@app.get("/")
async def root():
    return {"message": "Resume Parser API is running"}
