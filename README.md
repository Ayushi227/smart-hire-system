# 🤖 Smart Hire System

An AI-powered interview automation platform that evaluates candidates through resume parsing, personality prediction, facial emotion recognition, and speech tone analysis — all in one pipeline.

---

## 📌 Overview

Smart Hire System streamlines the hiring process by automating candidate evaluation. Candidates complete an online interview by recording video responses to three standard questions. The system then analyzes their resume, predicts their personality type, transcribes their speech, analyzes tone, and detects facial emotions — giving interviewers a comprehensive data-driven profile.

---

## ✨ Features

- **Candidate Registration & Interviewer Login** — Separate portals for candidates and HR interviewers
- **Resume Parsing** — Extracts name, skills, degree, designation, experience, and contact details using `pyresparser`
- **Personality Prediction** — Predicts personality type (Big Five traits) using Logistic Regression trained on survey data
- **Video Interview Recording** — Candidates record responses to 3 interview questions directly in the browser
- **Speech-to-Text Transcription** — Uploads video to AWS S3 and transcribes using Amazon Transcribe
- **Tone Analysis** — Analyzes transcribed text for Analytical, Confident, Fear, Joy, and Tentative tones using IBM Watson Tone Analyzer
- **Facial Emotion Recognition (FER)** — Detects emotions frame-by-frame across all 3 videos using `fer` with MTCNN
- **Result Dashboard** — Displays candidate profile, answers, tone charts, and emotion graphs to the interviewer
- **Automated Email** — Sends acceptance or rejection emails to candidates directly from the platform

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| Database | MySQL |
| ML Model | Scikit-learn (Logistic Regression) |
| Resume Parsing | pyresparser, spaCy |
| Speech-to-Text | AWS Transcribe + boto3 |
| Tone Analysis | IBM Watson Tone Analyzer |
| Emotion Detection | FER (MTCNN), OpenCV |
| Email | Flask-Mail (Gmail SMTP) |
| Data & Plotting | NumPy, Pandas, Matplotlib, Seaborn |

---

## 📁 Project Structure

```
smart-hire-system/
├── app.py                  # Main Flask application & all routes
├── video_analysis.py       # AWS Transcribe + IBM Watson tone analysis
├── test.py                 # Standalone script to test personality prediction
├── requirements.txt        # Python dependencies
├── static/
│   ├── trainDataset.csv    # Big Five personality training data
│   ├── result.json         # Candidate result (generated at runtime)
│   ├── answers.json        # Interview answers (generated at runtime)
│   ├── tone_analysis.jpg   # Tone analysis chart (generated at runtime)
│   ├── fer_output.png      # Emotion recognition chart (generated at runtime)
│   └── combined.webm       # Merged interview video (generated at runtime)
└── templates/
    ├── index.html          # Landing page (signup/login)
    ├── FirstPage.html      # Candidate dashboard
    ├── questionPage.html   # Interview recording page
    ├── recorded.html       # Interview complete confirmation
    ├── candidateSelect.html # Interviewer candidate selection
    └── result.html         # Candidate results dashboard
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11 (required — spaCy 2.3.5 is not compatible with Python 3.12+)
- MySQL server running locally
- AWS account with S3 and Transcribe access
- IBM Watson Tone Analyzer instance
- A Gmail account for sending emails

### 1. Clone the Repository

```bash
git clone https://github.com/Ayushi227/smart-hire-system.git
cd smart-hire-system
```

### 2. Create a Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Set Up the Database

Create a MySQL database and a candidates table:

```sql
CREATE DATABASE smarthire;
USE smarthire;

CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidatename VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# MySQL
mysql_user=your_mysql_username
mysql_password=your_mysql_password

# Gmail (for sending emails)
mail_username=your_gmail@gmail.com
mail_pwd=your_gmail_app_password

# Interviewer login credentials
company_mail=hr@yourcompany.com
company_pswd=your_portal_password

# AWS
aws_access_key_id=your_aws_access_key
aws_secret_key=your_aws_secret_key
my_region=us-east-1
bucket_name=your_s3_bucket_name
lang_code=en-US

# IBM Watson
ibm_apikey=your_ibm_watson_apikey
ibm_url=your_ibm_watson_service_url
```

> **Note:** For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) rather than your regular password.

### 6. Run the App

```bash
python app.py
```

Visit **http://127.0.0.1:5000** in your browser.

---

## 🔄 How It Works

### Candidate Flow
1. **Sign up** on the landing page
2. **Fill in personal details** and upload resume — the system parses the resume and predicts personality
3. **Record video answers** to 3 interview questions in the browser
4. Receives a **confirmation screen** once the interview is submitted

### Interviewer Flow
1. **Log in** with company credentials
2. **Select a candidate** to review
3. Views the full **results dashboard** — resume data, personality prediction, interview answers, tone analysis chart, and facial emotion recognition graph
4. Clicks **Accept** or **Reject** to send an automated email to the candidate

---

## 🧠 ML & AI Components

### Personality Prediction
Uses a **Multinomial Logistic Regression** model trained on `trainDataset.csv`. Input features are gender, age, and scores for the Big Five personality traits: Openness, Neuroticism, Conscientiousness, Agreeableness, and Extraversion. The model outputs a predicted personality type label.

### Speech-to-Text (AWS Transcribe)
Each recorded `.webm` video is uploaded to an S3 bucket. An asynchronous AWS Transcribe job converts the audio to text and returns a JSON transcript. The bucket is cleared after each use.

### Tone Analysis (IBM Watson)
The transcribed text for each question is sent to IBM Watson Tone Analyzer, which scores it across five tones: Analytical, Confident, Fear, Joy, and Tentative. Results are plotted as a grouped bar chart per question.

### Facial Emotion Recognition (FER)
All three video recordings are merged into a single video using OpenCV. The `fer` library with MTCNN face detection then processes the combined video frame by frame, tracking emotions (angry, disgust, fear, happy, sad, surprise, neutral) over time and saving a line graph of the results.

---

## 📦 Dependencies

```
numpy, scipy, pandas, matplotlib, seaborn
scikit-learn
opencv-python
Flask, Flask-Mail, flask-mysqldb
boto3
ibm_watson, ibm-cloud-sdk-core
python-dotenv, python-decouple
nltk
spacy==2.3.5
tensorflow
fer
pyresparser
```

---

## ⚠️ Known Issues & Notes

- **Python version:** Must use Python 3.11. `spacy==2.3.5` and `blis` (a spaCy dependency) do not build on Python 3.12+.
- **AWS costs:** Amazon Transcribe is a paid service. Each transcription job incurs a small cost based on audio duration.
- **Transcription delay:** The app waits 45 seconds between polling the transcription job status, so the analysis step takes several minutes to complete.
- **Windows path:** `trainDataset.csv` is referenced with a Windows-style path (`static\trainDataset.csv`). On Mac/Linux, change this to `static/trainDataset.csv` in `app.py` and `test.py`.
- **Gender hardcoded:** The gender field in the prediction route is currently hardcoded to `'female'`. The form input exists but is not wired up.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
