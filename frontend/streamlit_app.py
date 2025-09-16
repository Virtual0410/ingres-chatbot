# frontend/streamlit_app.py
import streamlit as st
import json
import difflib
from pathlib import Path
from datetime import datetime
import os
os.makedirs("data", exist_ok=True)

import requests
from requests.exceptions import RequestException

# small helper to send chat logs to backend without blocking the UI
def send_chatlog(role: str, message: str):
    """
    Send chat message to backend /chatlog/ endpoint.
    Uses a short timeout and swallows errors so the UI never breaks if backend is down.
    """
    try:
        # We use params because backend expects query params in the current implementation
        requests.post("http://127.0.0.1:8000/chatlog/", params={"role": role, "message": message}, timeout=1)
    except RequestException:
        # fail silently — we don't want to break the frontend if backend is offline
        pass


st.set_page_config(page_title="INGRES Assistant (Prototype)", layout="wide")

with st.sidebar:
    st.header("Quick Links")
    st.markdown("[INGRES Website](https://ingres.iith.ac.in/home)")
    st.markdown("[Groundwater Reports](#)")
    st.markdown("[User Manual PDF](#)")

# Load FAQ
FAQ_PATH = Path("data/faq.json")
if not FAQ_PATH.exists():
    st.error("Missing data/faq.json — ask data team to add it.")
    st.stop()

with open(FAQ_PATH, "r", encoding="utf-8") as f:
    faq = json.load(f)

questions = [item["question"] for item in faq]

# --- helpers ---
def find_best_match(query, cutoff=0.55):
    for item in faq:
        if query.strip().lower() == item["question"].strip().lower():
            return item, 1.0
    matches = difflib.get_close_matches(query, questions, n=1, cutoff=cutoff)
    if matches:
        matched_q = matches[0]
        for item in faq:
            if item["question"] == matched_q:
                ratio = difflib.SequenceMatcher(None, query, matched_q).ratio()
                return item, ratio
    return None, 0.0

def search_faq(keyword):
    return [
        item for item in faq
        if keyword.lower() in item["question"].lower() or keyword.lower() in item["answer"].lower()
    ]

# init chat history
if "history" not in st.session_state:
    st.session_state.history = []

# layout
st.title("INGRES Assistant — Prototype")
st.markdown("**Built-in quick questions** — click a chip to auto-fill and get the pre-written answer.")

# assume questions is a list of suggestions, e.g. from faq.json

with open("data/faq.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

questions = [item["question"] for item in faq_data]

# create 3 columns for buttons
cols = st.columns(3)

for i, q in enumerate(questions[:9]):  # show first 9 in 3 columns
    with cols[i % 3]:
        if st.button(q, key=f"q_{i}"):
            # user clicked a suggested question
            item, score = find_best_match(q)

            # 1) append user message to chat history
            st.session_state.history.append({"role": "user", "text": q})

            # 2) send user message to backend (non-blocking)
            send_chatlog("user", q)

            # 3) determine bot reply and append
            if item:
                bot_text = item["answer"]
                st.session_state.history.append(
                    {"role": "bot", "text": bot_text, "score": score, "source": item.get("source", "")}
                )

                # 4) send bot reply to backend
                send_chatlog("bot", bot_text)
            else:
                fallback = "I don't have that information yet. Would you like me to create an escalation ticket?"
                st.session_state.history.append(
                    {"role": "bot", "text": fallback, "score": 0.0, "source": ""}
                )
                send_chatlog("bot", fallback)

# unified search
search_input = st.text_input("🔍 Search or ask a question")

if search_input:
    st.session_state.history.append({"role": "user", "text": search_input})

    # 1. exact/fuzzy match
    item, score = find_best_match(search_input)
    if item and score > 0.55:
        st.session_state.history.append({"role": "bot", "text": item["answer"], "score": score, "source": item.get("source", "")})

    else:
        # 2. keyword search
        results = search_faq(search_input)
        if results:
            answer_texts = "\n".join([f"Q: {r['question']}\nA: {r['answer']}" for r in results])
            st.session_state.history.append({"role": "bot", "text": answer_texts, "score": 0.4, "source": ""})
        else:
            # 3. fallback to escalation
            if "last_query" not in st.session_state:
                st.session_state.last_query = ""
            st.session_state.last_query = search_input

            st.warning("I couldn’t find an answer. Please fill escalation form below:")

            with st.form("escalation_form"):
                st.subheader("Escalation Form")
                name = st.text_input("Name")
                email = st.text_input("Email")
                report_id = st.text_input("Report ID")
                issue = st.text_area("Describe your issue")
                submitted = st.form_submit_button("Submit")

                if submitted:
                    payload = {
                        "name": name,
                        "email": email,
                        "issue": issue,
                        "report_id": report_id
                    }
                    try:
                        res = requests.post("http://127.0.0.1:8000/escalation/", params=payload)
                        if res.status_code == 200:
                            st.success("Escalation submitted successfully!")
                        else:
                            st.error("Error submitting escalation")
                    except Exception as e:
                        st.error(f"Backend not reachable: {e}")


# show chat history
for turn in st.session_state.history[::-1]:
    if turn["role"] == "bot":
        with st.chat_message("assistant"):
            st.markdown(f"**INGRES Assistant** — confidence: {turn.get('score', 0):.2f}")
            st.markdown(turn["text"])
            if turn.get("source"):
                st.caption(f"Source: {turn.get('source')}")
    else:
        with st.chat_message("user"):
            st.markdown(turn["text"])

# # activity log download
# if st.button("Download chat log"):
#     import io
#     log = "\n".join([f"{datetime.now().isoformat()} - {h['role']}: {h['text']}" for h in st.session_state.history])
#     b = io.BytesIO(log.encode())
#     st.download_button("Download log file", b, file_name="chat_log.txt")

# Callback function to clear the history
def clear_chat_history():
    st.session_state.history = []
st.button('Clear chat history', on_click=clear_chat_history)
