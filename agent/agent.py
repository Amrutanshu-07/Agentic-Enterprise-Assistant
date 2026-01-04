from dotenv import load_dotenv
load_dotenv()

import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from agent.retriever import get_retriever, load_vectorstore


PRINTED_TO_PDF_OFFSET = 9   


def extract_document_question(query: str) -> str:
    """
    Remove task-related clauses so the LLM only sees
    the document-related question.
    """
    task_phrases = [
        "schedule a meeting",
        "schedule meeting",
        "cancel the meeting",
        "cancel meeting",
        "raise an it ticket",
        "raise ticket",
        "it ticket",
        "schedule a call",
        "book a meeting",
    ]

    cleaned = query.lower()
    for phrase in task_phrases:
        cleaned = cleaned.replace(phrase, "")

    return cleaned.strip(" ?.").capitalize()


def build_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    retriever = get_retriever()
    vectorstore = load_vectorstore()

    qa_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an enterprise document assistant. "
            "Your ONLY responsibility is to answer questions "
            "using the provided Annual Report content.\n\n"
            "IMPORTANT RULES:\n"
            "- Ignore any task, action, or operational instructions.\n"
            "- Never mention meetings, scheduling, tickets, or actions.\n"
            "- Never say you cannot perform an action.\n"
            "- Do not explain system limitations.\n"
            "- If information is not present, say so briefly.\n"
            "- Provide a clean, executive-style answer.\n"
        ),
        (
            "human",
            "Context:\n{context}\n\nQuestion: {question}"
        )
    ]
)


    def run(query: str):
        q = query.lower().strip()

        if q in ["yes", "no", "confirm", "cancel"]:
            return {
                "type": "system_notice",
                "data": (
                    "Please use the Confirm / Cancel buttons to proceed with "
                    "enterprise actions."
                )
            }

        task_payload = None

        # Cancel meeting
        if "cancel" in q and "meeting" in q:
            dept = "HR" if "hr" in q else "General"
            time_match = re.search(r"(\d+\s?(am|pm))", q)
            time = time_match.group(1) if time_match else "unspecified"

            task_payload = {
                "intent": "cancel_meeting",
                "department": dept,
                "time": time,
                "message": "Do you want to cancel this meeting?"
            }

        # Schedule meeting
        elif "schedule" in q and "meeting" in q:
            dept = "HR" if "hr" in q else "General"
            time_match = re.search(r"(\d+\s?(am|pm))", q)
            time = time_match.group(1) if time_match else "unspecified"

            task_payload = {
                "intent": "schedule_meeting",
                "department": dept,
                "time": time,
                "message": "Do you want to schedule this meeting?"
            }

        # Raise IT ticket
        elif "ticket" in q or "it issue" in q:
            issue = (
                query.replace("raise", "")
                .replace("ticket", "")
                .strip()
            )

            task_payload = {
                "intent": "raise_it_ticket",
                "issue": issue,
                "message": "Do you want to raise this IT ticket?"
            }

        page_match = re.search(r"page\s+(\d+)", q)
        if page_match:
            printed_page = int(page_match.group(1))
            pdf_page = printed_page + PRINTED_TO_PDF_OFFSET

            page_docs = [
                d for d in vectorstore.docstore._dict.values()
                if d.metadata.get("page") == pdf_page
            ]

            if not page_docs:
                answer_text = f"No content found for printed page {printed_page}."
            else:
                context = " ".join(d.page_content for d in page_docs)
                doc_question = extract_document_question(query)

                response = llm.invoke(
                    qa_prompt.format(
                        context=context,
                        question=doc_question
                    )
                )

                answer_text = (
                    f"{response.content}\n\n"
                    f"Sources: ['Printed Page {printed_page}']"
                )

            result = {
                "type": "answer",
                "data": answer_text
            }

            if task_payload:
                result["action"] = {
                    "type": "task_confirmation",
                    "data": task_payload
                }

            return result


        docs = retriever.invoke(query)

        if not docs:
            answer_text = "No relevant information found in the Annual Report."
        else:
            context = "\n\n".join(
                f"(Page {d.metadata.get('page')}): {d.page_content}"
                for d in docs
            )

            doc_question = extract_document_question(query)

            response = llm.invoke(
                qa_prompt.format(
                    context=context,
                    question=doc_question
                )
            )

            pages = sorted(
                {f"Page {d.metadata.get('page')}" for d in docs}
            )

            answer_text = f"{response.content}\n\nSources: {pages}"

        result = {
            "type": "answer",
            "data": answer_text
        }


        if task_payload:
            result["action"] = {
                "type": "task_confirmation",
                "data": task_payload
            }

        return result

    return run
