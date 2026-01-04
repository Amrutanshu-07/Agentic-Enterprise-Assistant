Agentic Enterprise Assistant 

An enterprise-grade Agentic AI system that combines Retrieval-Augmented Generation (RAG) with safe action orchestration to enable accurate document intelligence and controlled enterprise task execution.

This project was developed as part of an NLP Challenge, focusing on low hallucination, high accuracy, auditability, and real-world enterprise applicability.

Key Highlights:

✅ Answers questions strictly grounded in the HCLTech Annual Report

✅ Supports enterprise actions (meeting scheduling, cancellation, IT tickets)

✅ Explicit confirmation-based execution (no accidental actions)

✅ Page-level traceability for document answers

✅ Audit logging for all interactions and actions

✅ MCP (Model Context Protocol) integration for enterprise context

✅ Designed with production-grade architecture principles

System Architecture Overview:

The system follows a clear separation of concerns, inspired by real enterprise AI copilots.

User
 │
 ▼
Streamlit UI (Employee Dashboard)
 │
 ├── Document Query ──▶ RAG Pipeline ──▶ Grounded Answer
 │
 └── Action Intent ───▶ Agent Layer ───▶ Confirmation ───▶ Enterprise System

Architecture Layers:

Ingestion Layer – PDF → Chunks → Embeddings → Vector DB

Document Intelligence Layer (RAG) – Accurate, grounded answers

Agentic Orchestration Layer – Intent detection & task proposals

UI & Audit Layer – Confirmation, execution status, logging

Project Structure
agentic-enterprise-assistant/
│
├── data/
│   ├── hcltech_annual_report.pdf
│   └── faiss_index/
│
├── ingest/
│   ├── load_pdf.py
│   └── build_vector_db.py
│
├── agent/
│   ├── agent.py
│   ├── retriever.py
│   └── tools.py
│
├── mcp/
│   └── server.py
│
├── ui/
│   └── app.py
│
├── logs/
│   └── interactions.json
│
├── .env
├── requirements.txt
└── README.md

Core Components Explained
1️⃣ Ingestion Layer (ingest/)

Purpose: Convert the Annual Report PDF into a searchable knowledge base.

load_pdf.py

Extracts text page-by-page

Preserves page numbers for citations

build_vector_db.py

Splits text into overlapping chunks

Generates embeddings

Stores vectors in FAISS

⚠️ Run this once before starting the application.

python ingest/build_vector_db.py

2️⃣ Document Intelligence (RAG)

Purpose: Answer queries strictly based on the Annual Report.

Uses semantic search over FAISS

Retrieves only relevant document chunks

LLM reasons only on retrieved context

Prevents hallucination and guessing

Example Query:

What was the revenue growth in FY25?

3️⃣ Agentic Orchestration Layer

Purpose: Detect and manage enterprise actions safely.

Supported actions:

Schedule meeting

Cancel meeting

Raise IT ticket

Key Design Principles:

The AI does not execute actions directly

Actions are proposed as structured JSON

Execution requires explicit user confirmation

Delegation is done to enterprise systems (conceptually)

Example Action Proposal:

{
  "intent": "schedule_meeting",
  "department": "HR",
  "time": "11am"
}

4️⃣ MCP Integration (mcp/)

What is MCP?
Model Context Protocol (MCP) provides a standardized way to expose enterprise context, policies, and capabilities to AI systems.

Why MCP is used:

Separates business rules from agent logic

Enables centralized governance

Future-ready for multi-agent systems

Avoids hard-coded enterprise assumptions

Run MCP server:

python mcp/server.py

5️⃣ User Interface (ui/app.py)

Built with Streamlit

The employee dashboard includes:

Query Input Section

Single input for document questions or commands

Document Answer Panel

Clean, executive-style answers

Page citations where applicable

Action Confirmation Panel

Appears only when an action is detected

Confirm / Cancel buttons only (no free-text)

Execution Status Panel

Displays completion or cancellation

Timestamped status

Audit Visibility Panel

Shows recent interactions and actions

Run the UI:

streamlit run ui/app.py

Audit Logging

All interactions are logged in:

logs/interactions.json


Each log entry contains:

Timestamp

User query

System response

Action intent (if any)

Execution status

This supports:

Traceability

Compliance review

Debugging

Environment Setup
1️⃣ Create .env file
GOOGLE_API_KEY=your_gemini_api_key_here


⚠️ Do not commit .env to version control.

2️⃣ Install Dependencies
pip install -r requirements.txt


Recommended: use a virtual environment or conda environment.

🚀 How to Run (Step-by-Step)
# Step 1: Build vector database
python ingest/build_vector_db.py

# Step 2: (Optional) Run MCP server
python mcp/server.py

# Step 3: Launch UI
streamlit run ui/app.py

Example Queries for Demo

Document Queries

What was the revenue growth in FY25?

What are the key risk factors mentioned in the Annual Report?

Enterprise Actions

Schedule a meeting with HR

Cancel the HR meeting at 11am

Raise an IT ticket for VPN access

Dual-Intent Query

What was the revenue growth in FY25? Schedule a meeting with HR.
