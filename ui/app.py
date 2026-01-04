import sys
import os
import json
from datetime import datetime


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agent.agent import build_agent



LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "interactions.json")

os.makedirs(LOG_DIR, exist_ok=True)


def save_to_json(query, response):
    """Persist each interaction in a JSON file"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "response": response,
        "type": response.get("type", "unknown") if isinstance(response, dict) else "text"
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)


st.set_page_config(
    page_title="Agentic Enterprise Assistant – HCLTech",
    page_icon="🤖",
    layout="wide"
)

with st.sidebar:
    st.title("📊 Enterprise Assistant")
    st.markdown("""
 
**System Type:** Assistant  

**Core Capabilities**
- Annual Report Q&A
- Page-level citations
- Dual-intent handling
- HR / IT task proposals
- Confirmation-based execution
- Audit logging
""")
    st.markdown("---")
    st.caption("Your Assistant")


if "pending_task" not in st.session_state:
    st.session_state.pending_task = None

st.title("🤖 Agentic Enterprise Assistant")
st.subheader("Annual Report Intelligence System")

st.markdown(
    """
Ask questions or give commands.
"""
)

@st.cache_resource
def load_agent():
    return build_agent()

agent = load_agent()

query = st.text_input(
    "💬 Enter your query or command",
    placeholder="e.g. What was the revenue growth in FY25? Schedule a meeting with HR."
)


if query:
    if query.lower().strip() in ["yes", "no", "confirm", "cancel"] and st.session_state.pending_task:
        st.warning("⚠️ Please use the Confirm / Cancel buttons below to proceed.")
        st.stop()

    with st.spinner("Processing..."):
        response = agent(query)

    save_to_json(query, response)

    st.markdown("### 🧾 Response")


    if isinstance(response, dict) and response.get("type") == "system_notice":
        st.info(response["data"])


    elif isinstance(response, dict) and response.get("type") == "answer":
        st.markdown("#### 📄 Answer from Annual Report")
        st.markdown(response["data"])


        if "action" in response:
            st.markdown("---")
            st.warning("⚙️ Action Confirmation Required")

            action = response["action"]["data"]
            st.json(action)

            st.session_state.pending_task = action

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Confirm"):
                    task = st.session_state.pending_task.copy()
                    task["status"] = "completed"
                    task["executed_at"] = datetime.now().isoformat()

                    save_to_json("CONFIRM_ACTION", task)

                    st.success("Task executed successfully")
                    st.json(task)

                    st.session_state.pending_task = None

            with col2:
                if st.button("❌ Cancel"):
                    cancelled = {
                        "status": "cancelled",
                        "task": st.session_state.pending_task.get("intent")
                    }

                    save_to_json("CANCEL_ACTION", cancelled)

                    st.info("Task cancelled")
                    st.json(cancelled)

                    st.session_state.pending_task = None


    else:
        st.write(response)

st.markdown("---")
st.caption("Enterprise RAG System with Safe Action Execution & Audit Logging")
