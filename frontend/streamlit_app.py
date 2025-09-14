# frontend/streamlit_app.py
import streamlit as st
import json
import difflib
from pathlib import Path
from datetime import datetime
import os
os.makedirs("data", exist_ok=True)

st.set_page_config(page_title="INGRES Assistant (Prototype)", layout="wide")

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

# suggestion chips
cols = st.columns(3)
for i, q in enumerate(questions[:9]):
    with cols[i % 3]:
        if st.button(q, key=f"q_{i}"):
            item, score = find_best_match(q)
            if item:
                st.session_state.history.append({"role": "user", "text": q})
                st.session_state.history.append({"role": "bot", "text": item["answer"], "score": score, "source": item.get("source", "")})

st.write("---")

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
                user_name = st.text_input("Your Name")
                user_email = st.text_input("Your Email")
                category = st.selectbox("Issue Category", ["Data Access", "Report Issue", "Quality Parameters", "Login Problem", "Other"])
                details = st.text_area("Describe your issue")
                submitted = st.form_submit_button("Submit")

                if submitted:
                    import csv, uuid
                    ticket_id = str(uuid.uuid4())[:8]
                    with open("data/escalations.csv", "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([ticket_id, user_name, user_email, category, st.session_state.last_query, details])
                    st.success(f"✅ Your issue has been escalated. Ticket ID: {ticket_id}")

# show chat history
for turn in st.session_state.history[::-1]:
    if turn["role"] == "bot":
        st.markdown(f"**INGRES Assistant** — confidence: {turn.get('score', 0):.2f}")
        st.info(turn["text"])
        if turn.get("source"):
            st.caption(f"Source: {turn.get('source')}")
    else:
        st.write(f"**You:** {turn['text']}")

# activity log download
if st.button("Download chat log"):
    import io
    log = "\n".join([f"{datetime.now().isoformat()} - {h['role']}: {h['text']}" for h in st.session_state.history])
    b = io.BytesIO(log.encode())
    st.download_button("Download log file", b, file_name="chat_log.txt")
