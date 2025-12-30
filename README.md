
#  FastAPI + n8n Job Alert Automation

An end-to-end **resume-aware job alert system** that automatically parses resumes, scans live job listings, matches them against user skills, and sends real-time notifications when relevant jobs are found.

---

##  Why this project?

Searching for jobs manually is repetitive and inefficient.
This project automates the entire process by:

* Understanding **your resume**
* Continuously scanning **live job feeds**
* Matching jobs based on **skills, education, and experience**
* Notifying you **only when a relevant job appears**

##  Key Features

* Resume-aware automation
* Real-time job alerts
* Modular workflow design
* Scalable & production-ready
* No manual job searching
* Clean separation of concerns

---

##  Architecture

Resume Upload (FastAPI)
        ↓
Resume Parsing
        ↓
n8n Webhook
        ↓
Resume Storage (Static Data)
        ↓
Scheduled Job Scans
        ↓
Skill Matching
        ↓
Job Alerts


##  Tech Stack

* **FastAPI** – Resume upload & parsing service
* **n8n** – Automation, scheduling, logic orchestration
* **RSS Feeds / APIs** – Live job sources
* **Telegram / Messaging** – Job notifications
* **Python** – Resume processing
* **JavaScript (n8n Code Nodes)** – Matching logic



##  Project Structure

fastapi-n8n-job-alert-automation/
│
├── main.py                 # FastAPI backend
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore
└── n8n/
    └── workflow.json       # Exported n8n workflow


##  What FastAPI Does

FastAPI acts as the **entry point** of the system.

### Responsibilities:

* Accepts resume uploads (PDF)
* Extracts:

  * Skills
  * Education level
  * Experience level
* Converts resume into **structured JSON**
* Sends this data to **n8n via Webhook**

### Why FastAPI?

* Extremely fast
* Async & scalable
* Clean API design
* Perfect for microservices

---

##  How FastAPI Connects to n8n

FastAPI sends parsed resume data to n8n using an **HTTP POST Webhook**.

Example payload sent to n8n:

json
{
  "skills": ["python", "fastapi", "sql"],
  "education_level": "Bachelor's",
  "experience_level": "Junior (2–4 years)"
}


This webhook **triggers the n8n workflow automatically**.

---

##  n8n Workflow Overview

The n8n workflow is intentionally designed with **two independent branches** inside a single workflow.

This separation ensures **clarity, reliability, and scalability**.

---

##  Branch 1: Resume Update Branch (Event-Driven)

 **Triggered by:** FastAPI Webhook


Webhook → Save Resume to Static Data


### What this branch does:

* Receives resume data from FastAPI
* Stores the **latest resume** in n8n’s Static Data
* Overwrites older resume automatically
* Acts as the **single source of truth**

### Why this branch exists:

* Resume changes are **event-based**
* Job scanning should not run every time a resume is uploaded
* Keeps resume handling clean and isolated


##  Branch 2: Job Matching Branch (Time-Driven)

 **Triggered by:** n8n Schedule Trigger

Schedule → Load Resume → Fetch Jobs → Match Skills → IF → Send Alert


### What this branch does:

* Runs automatically (every 15mins)
* Loads the **latest resume**
* Fetches live job listings
* Matches jobs against resume skills
* Filters only relevant jobs
* Sends notifications

### Why this branch exists:

* Job searching is a **continuous process**
* Must run independently of resume uploads
* Prevents unnecessary executions

---

##  Why Two Branches Are Important

| Resume Updates  | Job Scanning          |
| --------------- | --------------------- |
| Event-based     | Time-based            |
| Rare            | Frequent              |
| Lightweight     | Heavy                 |
| One-time action | Continuous automation |

This design mirrors **real-world production systems**.

---

##  Skill Matching Logic (Simplified)

For each job:

* Extract job description
* Compare with resume skills
* Calculate match score
* Decide if it’s a strong match

Only jobs that pass the criteria move forward.

---

##  Notifications

When a job matches:

* A message is sent automatically (Telegram / messaging)
* Includes:

  * Job title
  * Matched skills
  * Match score
  * Apply link

No spam. Only meaningful alerts.

---

##  n8n Workflow screenshot

<img width="1234" height="503" alt="Screenshot 2025-12-30 174541" src="https://github.com/user-attachments/assets/1c513df0-0dda-4444-b7bf-5c170a072fe5" />

##  Conclusion

This project demonstrates how **FastAPI and n8n can work together** to build a powerful automation system that feels intelligent, efficient, and practical.


 *Built with curiosity, automation, and clean design.*

----






