# frontend/streamlit_app.py
import streamlit as st
import json
import difflib
from pathlib import Path
from datetime import datetime

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
    # exact match first (case-insensitive)
    for item in faq:
        if query.strip().lower() == item["question"].strip().lower():
            return item, 1.0
    # fuzzy match using difflib
    matches = difflib.get_close_matches(query, questions, n=1, cutoff=cutoff)
    if matches:
        matched_q = matches[0]
        for item in faq:
            if item["question"] == matched_q:
                # compute ratio
                ratio = difflib.SequenceMatcher(None, query, matched_q).ratio()
                return item, ratio
    return None, 0.0

# init chat history
if "history" not in st.session_state:
    st.session_state.history = []

# --- search helper ---
def search_faq(keyword):
    results = []
    for item in faq:
        if keyword.lower() in item["question"].lower() or keyword.lower() in item["answer"].lower():
            results.append(item)
    return results

# layout
st.title("INGRES Assistant — Prototype")
st.markdown("**Built-in quick questions** — click a chip to auto-fill and get the pre-written answer.")

# suggestion chips
cols = st.columns(3)
for i, q in enumerate(questions[:9]):  # show first 9 in 3 cols
    with cols[i % 3]:
        if st.button(q, key=f"q_{i}"):
            # add question -> get answer
            item, score = find_best_match(q)
            if item:
                st.session_state.history.append({"role": "user", "text": q})
                st.session_state.history.append({"role": "bot", "text": item["answer"], "score": score, "source": item.get("source","")})

st.write("---")

# --- unified search (autocomplete + keyword) ---
search_input = st.text_input("🔍 Search or ask a question", key="unified_search")

if search_input:
    # 1. Autocomplete check (exact/close match in question list)
    matched_qs = [q for q in questions if search_input.lower() in q.lower()]

    if matched_qs:
        st.subheader("📌 Suggestions")
        for mq in matched_qs:
            st.write(f"**Q:** {mq}")
            for item in faq:
                if item["question"] == mq:
                    st.caption(item["answer"])
    else:
        # 2. Fallback → keyword search in Q & A
        results = search_faq(search_input)
        if results:
            st.subheader("🔎 Results")
            for r in results:
                st.write(f"**Q:** {r['question']}")
                st.caption(r['answer'])
        else:
            st.warning("No results found.")

# show chat
for turn in st.session_state.history[::-1]:
    if turn["role"] == "bot":
        st.markdown(f"**INGRES Assistant** — confidence: {turn.get('score',0):.2f}")
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
