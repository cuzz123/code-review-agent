# 🔍 AI Code Review Agent

> AI-powered code review tool that analyzes code from 4 dimensions: architecture, security, performance, and style.
> Built with LangChain, FastMCP, FastAPI, and Streamlit.

## ✨ Features

- **4-Dimension Review** — Architecture, Security, Performance, Style
- **Score & Report** — 0-100 scoring with structured issue list
- **Real-time UI** — Streamlit web interface
- **FastAPI Backend** — REST API for integration

## 🏗️ Architecture

```
User Input (code) → Supervisor → 4 Workers → Report
                                   ├─ Architecture
                                   ├─ Security
                                   ├─ Performance
                                   └─ Style
```

## 🚀 Quick Start

```bash
git clone https://github.com/cuzz123/code-review-agent.git
cd code-review-agent

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start backend
uvicorn app.api:app --reload --port 8000

# Start frontend (separate terminal)
streamlit run app/ui.py --server.port 8501
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Orchestration | LangChain + Supervisor-Worker |
| LLM | DeepSeek Chat |
| Backend | FastAPI |
| Frontend | Streamlit |
| Data Models | Pydantic |

## 📁 Project Structure

```
code-review-agent/
├── app/
│   ├── api.py            # FastAPI endpoints
│   ├── ui.py             # Streamlit frontend
│   ├── models.py         # Pydantic schemas
│   ├── workers.py        # 4 review workers
│   ├── supervisor.py     # Orchestrator + scoring
│   └── tools/
│       └── code_analyzer.py
├── data/samples/
│   └── bad_code.py
└── requirements.txt
```

## 📝 License

MIT
