# 🛡️ LegalGuard AI Pro
### Neural Audit & Risk Quantification Dashboard

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

LegalGuard AI Pro is a sophisticated **Legal-Tech Web Application** designed to automate the analysis of complex legal documents. By utilizing **Neural Linguistic Patterns**, the system extracts "Red Flag" clauses and provides a quantified safety rating (0-100) for PDFs, Web URLs, and Manual Text.

---

## 🚀 Key Features
* **Multi-Source Input:** Seamlessly audit raw text, live website URLs, or uploaded PDF documents.
* **Neural Risk Matrix:** Categorized threat levels (High/Medium) based on machine learning confidence.
* **Evidence Extraction:** Real-time extraction of specific problematic quotes like "Forced Arbitration" or "Liability Gaps".
* **Enterprise UI:** A professional dark-mode dashboard built with Streamlit and custom CSS.

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Python-based Web Framework).
* **Backend Engine:** [FastAPI](https://fastapi.tiangolo.com/) (REST API).
* **Communication:** `requests` (JSON payload bridging).
* **Processing:** NLP (Natural Language Processing) & Web Scraping.

## 🏗️ Technical Architecture
The project follows a **Decoupled Microservice Architecture**:
1. **Client Layer (Streamlit):** Manages user session state and input validation.
2. **API Bridge:** Handles multipart/form-data for PDF uploads and text-based POST requests.
3. **Neural Engine (FastAPI):** The backend engine that runs the linguistic analysis models.

## 🚦 Getting Started
1. **Clone the repo:**
   ```bash
   git clone https://github.com/priya-kothamasu/legal-guard-pro.git
  