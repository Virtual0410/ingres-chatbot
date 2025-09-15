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

## 📂 Project Structure
<pre>
ingres-chatbot/<br>
├── backend/<br>
  ├── db.py # Database connection & setup<br>
  ├── models.py # Data models (SQLAlchemy)<br>
  └── fastapi_app.py # FastAPI server stub<br>
├── data/<br>
  └── faq.json # Initial FAQ data<br>
├── datasets/ # Folder for CSV data files<br>
├── frontend/<br>
  └── streamlit_app.py # Main chatbot UI<br>
├── chatbot.db # SQLite database (auto-generated)<br>
├── .gitignore<br>
├── requirements.txt<br>
└── README.md
</pre>