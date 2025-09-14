# INGRES Chatbot (SIH prototype)

Day 1: basic Streamlit UI + built-in FAQs.

Structure:
- frontend/streamlit_app.py
- backend/ (empty for Day1)
- data/faq.json

Team Workflow on Github:

1) git clone <url>
2) git checkout -b their-feature-branch (create their own branch)
3) Make changes, then 
    git add . , 
    git commit -m "message", 
    git push origin their-feature-branch
4) On GitHub, create a Pull Request from their-feature-branch into main.
5) git checkout main and git pull origin main to get the latest, merged code

Run:
1. python -m venv venv
2. venv\Scripts\activate.bat
3. pip install -r requirements.txt
4. streamlit run frontend/streamlit_app.py