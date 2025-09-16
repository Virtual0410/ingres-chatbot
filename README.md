# INGRES Chatbot (SIH prototype)

Day 1: basic Streamlit UI + built-in FAQs.

## Team Workflow on Github:

1.  `git clone <url>`
2.  `git checkout -b their-feature-branch` (create their own branch)
3.  Make changes, then  
    `git add .` ,  
    `git commit -m "message"`,  
    `git push origin their-feature-branch`
4.  On Github, create a Pull Request from `their-feature-branch` into `main`.
5.  `git checkout main` and `git pull origin main` to get the latest, merged code.

## Run:
1.  python -m venv venv
2.  venv\Scripts\activate.bat
3.  pip install -r requirements.txt
4.  streamlit run frontend/streamlit_app.py

---

## Day 2 Progress:
-   Added 20+ FAQs in `data/faq.json`
-   Clickable suggestions for quick queries
-   Fuzzy matching for typed questions
-   Escalation form to log unresolved queries (`data/escalations.txt`)
-   Simple UI polish (icons, colors, captions)
-   Backend placeholder created in `backend/fastapi_app.py` (to be used from Day 3)

## Day 3 Progress:
-   **Added a SQLite database** (`chatbot.db`) for structured data storage.
-   **Store escalation form submissions into DB** (replaces `escalations.txt`).
-   **Store chat history into DB** (optional, for demo and analytics).
-   **Introduced a backend folder** with FastAPI stub ("Hello World" + test endpoint).
-   **Streamlit now talks directly to DB** (backend will connect in Day-4).

## Day 4 Progress:

- Chat window styled + scrollable + avatars.
- Sidebar polished with links + about section.
- FAQ expanded with synonyms.
- Fuzzy search improved with fallback/“did you mean”.
- Backend GET endpoints (`/chatlog/all`, `/escalations/`).

## 📂 Project Structure
<pre>
ingres-chatbot/
│
├── backend/
│   ├── main.py             # FastAPI app (chatlog + escalation endpoints)
│   ├── db.py               # SQLite connection + table creation
│   └── models.py           # (optional) DB schema helpers
│
├── frontend/
│   ├── streamlit_app.py    # Main Streamlit chatbot app
│   ├── pages/
│   │   └── About.py        # Streamlit “About INGRES” page
│   └── components/         # (optional, custom widgets later)
│
├── data/
│   └── faq.json            # Predefined Q&A pairs
│
├── ingres.db               # SQLite database (auto-created)
│
├── requirements.txt        # Python dependencies
├── README.md               # Documentation (Day-4 deliverable)
└── .gitignore              # Ignore venv, __pycache__, ingres.db etc
</pre>