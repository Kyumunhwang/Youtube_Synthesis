# 📺 YouTube Intelligence Studio & Synthesis Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![AI Engine: Gemini 2.5 Flash](https://img.shields.io/badge/AI%20Engine-Gemini%202.5%20Flash-orange.svg)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A high-performance, responsive web application for searching, extracting, synthesizing, and archiving YouTube video intelligence without downloading large media files. Features neural multi-video synthesis powered by **Google Gemini 2.5 Flash** with an automatic heuristic zero-API fallback, one-click export to **Google Docs**, **MS-Word (.docx)**, and **HTML**, and persistent database indexing.

---

## ✨ Key Features

- **🔍 Smart Video Discovery & Card Grid**: Search YouTube or paste video URLs to preview cards with high-res thumbnails, durations, and channels.
- **⚡ Instant Subtitle Extraction**: Extracts clean plain text transcripts and timeline chapters in seconds without streaming video bytes (via `yt-dlp`).
- **🤖 Dual-Engine Synthesis**:
  - **Gemini 2.5 Flash Neural Engine**: Deep, paragraph-by-paragraph executive synthesis, comparative cross-analysis, and actionable implementation roadmaps.
  - **Zero-API Heuristic Synthesizer**: Built-in fallback ensuring full functionality even without an API key.
- **🚀 1-Click Google Docs Integration**: Seamlessly opens Google Docs and populates formatted reports ready for editing.
- **📥 Smart Multi-Format Export**: Generates semantic filenames (`YYYYMMDD_[Topic]_Synthesis_Report`) for `.docx`, `.html`, and `.md` downloads.
- **📚 Consolidated Knowledge Hub**: Select multiple stored records to generate synthesized reports or batch-delete outdated items.

---

## 🚀 1-Minute Web Cloud Deployment (Streamlit Community Cloud)

You can deploy this app to the web for free and access it from any browser, laptop, tablet, or smartphone.

### Step 1: Push Project to GitHub
In your local project folder:
```bash
# Initialize git if not already done
git init
git add .
git commit -m "feat: initial release of YouTube Intelligence Studio with Gemini AI"

# Create a new repository on GitHub (e.g., youtube-intelligence-studio)
# Then link and push:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Community Cloud (Free)
1. Visit **[share.streamlit.io](https://share.streamlit.io/)** and sign in with your GitHub account.
2. Click **"New app"**.
3. Select your repository, branch (`main`), and set **Main file path** to `app.py`.
4. Under **Advanced settings... > Secrets**, enter your Gemini API Key:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   ```
5. Click **"Deploy!"**. Your app is now live on a public or private web URL!

---

## 💻 Local Setup & Execution

### 1. Prerequisites
- Python 3.11 or newer
- Git

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env` and set your Gemini API key (obtain a free key from [Google AI Studio](https://aistudio.google.com/)):
```bash
cp .env.example .env
```
Inside `.env`:
```ini
GEMINI_API_KEY=AIzaSyYourSecretKeyHere
```

### 4. Run Application
```bash
streamlit run app.py
```
Or specify a custom port:
```bash
streamlit run app.py --server.port 3055
```

---

## 🔒 Security & Privacy Architecture

- **No Hardcoded Credentials**: API keys are dynamically loaded with strict hierarchy:
  1. UI Session input (temporary)
  2. Streamlit Cloud Secrets (`st.secrets["GEMINI_API_KEY"]`)
  3. Environment variables (`.env` via `python-dotenv`)
- **Git Shield**: `.env`, database storage files (`storage_db/`), and sensitive logs are excluded in `.gitignore`.
- **Zero-Storage Media**: Video/audio media files are never saved to disk, preserving storage and respecting copyright policies.

---

## 📁 Project Architecture

```
Scrapping/
├── app.py                  # Main Streamlit web application & view controller
├── ai_engine.py            # Google Gemini 2.5 Flash integration & prompt pipeline
├── extractor.py            # YouTube metadata & subtitle extraction engine
├── exporter.py             # Markdown to DOCX, styled HTML, and Google Docs launcher
├── storage.py              # Central database.json indexing & record manager
├── autopaste_docs.ps1      # Windows OS automation robot for Google Docs
├── requirements.txt        # Python dependency manifest
├── .gitignore              # Git exclusion rules
├── .env.example            # Environment variables template
├── .streamlit/
│   └── config.toml         # Streamlit visual theme and server settings
└── README.md               # Architecture and deployment documentation
```

---

## 📄 License
Released under the [MIT License](LICENSE).
