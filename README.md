
# IntelliSupport – AI-Powered IT Helpdesk Platform

## Overview

IntelliSupport is a hybrid AI-powered IT support platform that combines:
- Retrieval-Augmented Generation (RAG)
- Fine-Tuned Lightweight LLM (TinyLlama + QLoRA)
- Ticket Management System
- Role-Based Authentication
- Real-Time Chat Support

The system automates repetitive IT support tasks such as:
- Printer troubleshooting
- SQL Server connection issues
- PowerPoint support
- General Level-1 IT support queries

---

# Key Features

## AI Support Chatbot
- Interactive AI-powered support assistant
- Multi-turn conversation support
- Context-aware responses

## Dual AI Modes

### RAG Mode
- Retrieves information from domain-specific manuals
- Uses ChromaDB vector database
- Generates grounded responses using Gemini API

### Fine-Tuned Mode
- Uses TinyLlama-1.1B fine-tuned using QLoRA
- Local inference support
- Reduced API dependency

## Ticket Management
- Automatic escalation of unresolved issues
- Ticket creation and tracking
- Support dashboard for admins/staff

## Authentication & Roles
- JWT-based authentication
- User and Support Staff roles
- Protected routes

---

# Tech Stack

## Frontend
- React
- Vite
- Axios

## Backend
- FastAPI
- SQLAlchemy
- MySQL

## AI & NLP
- LangChain
- LangGraph
- ChromaDB
- Sentence Transformers
- TinyLlama
- QLoRA / LoRA
- Hugging Face Transformers
- Gemini API

---

# System Architecture

User → React Frontend → FastAPI Backend

Backend supports:
1. RAG Pipeline
2. Fine-Tuned TinyLlama Pipeline
3. Ticket Management System
4. MySQL Database

RAG Flow:
User Query → Embedding → ChromaDB Retrieval → Gemini Generation → Response

Fine-Tuned Flow:
User Query → TinyLlama Fine-Tuned Model → Response

---

# Dataset

Custom IT support dataset created using:
- Printer troubleshooting manuals
- SQL Server troubleshooting manuals
- PowerPoint support documentation

Dataset contains:
- Instruction-response pairs
- IT troubleshooting workflows
- Domain-specific support knowledge

---

# Fine-Tuning Details

## Base Model
TinyLlama/TinyLlama-1.1B-Chat-v1.0

## Fine-Tuning Method
QLoRA (Quantized Low-Rank Adaptation)

## Training Details
- 4-bit quantization
- LoRA adapters on q_proj and v_proj
- Rank: 16
- Alpha: 32
- Epochs: 2
- FP16 training

---

# Evaluation Metrics

The system was evaluated using:
- ROUGE-1
- ROUGE-2
- ROUGE-L
- BERTScore
- Keyword Coverage
- Manual Quality Evaluation

## Observations
- RAG achieved highest factual accuracy
- Fine-tuned model achieved faster local inference
- Hybrid system provided best overall flexibility

---

# Installation

## Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# Environment Variables

Create a `.env` file inside backend directory:

```env
GOOGLE_API_KEY=YOUR_API_KEY

db_user=root
db_password=YOUR_PASSWORD
db_host=localhost
db_port=3306
db_name=ai_support_db

secret_key=YOUR_SECRET_KEY
```

---

# Future Scope

- Voice-based support assistant
- Multilingual support
- Larger enterprise datasets
- Advanced ticket prioritization
- Deployment using Docker/Kubernetes
- Larger fine-tuned LLMs

---

# Conclusion

IntelliSupport demonstrates how modern NLP techniques such as RAG and parameter-efficient fine-tuning can be integrated into a real-world IT support workflow.

The project combines:
- AI engineering
- Full-stack development
- Information retrieval
- LLM fine-tuning
- Enterprise workflow automation

to create a practical intelligent support platform.

---

# Author

Priyakrith P S  
AI & Data Science  
IIIT Raichur
