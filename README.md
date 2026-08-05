# 🤖 IntelliReport AI

> **Production-Style Multi-Agent AI Report Generation System**

IntelliReport AI is a Multi-Agent AI application that automatically researches, plans, writes, improves, verifies, and reviews professional reports using Google's Gemini AI and LangGraph. The application provides a clean Streamlit interface with downloadable PDF and Word reports.

---

# 📌 Project Overview

IntelliReport AI is designed to automate the complete report generation process using multiple specialized AI agents. Instead of relying on a single prompt, the system divides the task into multiple intelligent stages, resulting in higher-quality, well-structured, and professionally reviewed reports.

The project demonstrates the practical implementation of Multi-Agent AI Systems using LangGraph.

---

# 🚀 Features

- 🔍 AI-powered Research Agent
- 📝 Automatic Report Outline Generation
- ✍ Professional Technical Report Writing
- 📝 Grammar & Language Improvement
- ✔ AI Fact Checking
- 📚 Automatic Citation Generation
- 🧐 AI Report Review
- 📊 Analytics Dashboard
- 📄 PDF Export
- 📝 Microsoft Word (.docx) Export
- 🎨 Professional Streamlit UI
- 🤖 Powered by Google Gemini AI
- 🔄 LangGraph Multi-Agent Workflow

---

# 🧠 Multi-Agent Workflow

```
User Input
      │
      ▼
┌──────────────────────┐
│  Research Agent      │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│  Outline Agent       │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│  Writer Agent        │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│  Grammar Agent       │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│ Fact Checker Agent   │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│ Citation Agent       │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│ Reviewer Agent       │
└──────────────────────┘
          │
          ▼
      Final Report
```

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Streamlit | Web Application |
| LangGraph | Multi-Agent Workflow |
| LangChain | LLM Integration |
| Google Gemini AI | Large Language Model |
| ReportLab | PDF Generation |
| python-docx | Word Export |
| Pillow | Image Processing |
| dotenv | Environment Variables |

---

# 📂 Project Structure

```
IntelliReport-AI
│
├── agents
│   ├── research_agent.py
│   ├── outline_agent.py
│   ├── writer_agent.py
│   ├── grammar_agent.py
│   ├── fact_checker_agent.py
│   ├── citation_agent.py
│   └── reviewer_agent.py
│
├── graph
│   ├── workflow.py
│   └── state.py
│
├── utils
│   ├── llm.py
│   ├── export_pdf.py
│   └── export_docx.py
│
├── assets
│   └── logo.jpg
│
├── app.py
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/IntelliReport-AI.git

cd IntelliReport-AI
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Run the Application

```bash
python -m streamlit run app.py
```

---

# 📊 Application Features

### ✅ Generate Professional Reports

Generate comprehensive AI-powered reports on any topic.

### ✅ AI Review

Automatically reviews generated reports for:

- Grammar
- Technical Accuracy
- Missing Sections
- Readability
- Professional Writing Style

### ✅ Analytics Dashboard

Displays:

- Execution Time
- Word Count
- Number of AI Agents Used

### ✅ Export Options

Download reports as:

- PDF
- Microsoft Word (.docx)

---

# 📸 Screenshots

Add screenshots here.

### Home Page

```
screenshots/home.png
```

### Generated Report

```
screenshots/report.png
```

### Analytics Dashboard

```
screenshots/analytics.png
```

### AI Review

```
screenshots/review.png
```

---

# 🔮 Future Enhancements

- User Authentication
- Report History
- Real-Time Web Search
- Multiple AI Model Support
- PowerPoint Export
- Citation using Research APIs
- Cloud Deployment
- Report Templates
- AI Chat Assistant

---

# 🎯 Learning Outcomes

This project demonstrates practical knowledge of:

- Multi-Agent AI Systems
- LangGraph
- LangChain
- Prompt Engineering
- LLM Orchestration
- Streamlit Development
- PDF Generation
- Word Document Generation
- AI Workflow Automation

---

# 👨‍💻 Authors

### Abhijeet Khot

SY MCA

MIT World Peace University

---

### Nivedita Deshpande

SY MCA

MIT World Peace University

---

# 👩‍🏫 Project Guide

**Mrs. Apoorva**

Faculty of MCA

MIT World Peace University

---

# 📄 License

This project is developed for academic purposes as part of the MCA Mini Project at MIT World Peace University.

---

# ⭐ Acknowledgements

- Google Gemini AI
- LangChain
- LangGraph
- Streamlit
- ReportLab
- Python Community

---

## 💡 IntelliReport AI

**"Transforming Ideas into Professional Reports through Multi-Agent Artificial Intelligence."**