from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import db, models

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

# Dependency
def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@app.get("/")
def root():
    return {"message": "INGRES backend running"}

@app.post("/escalation/")
def create_escalation(name: str, email: str, issue: str, report_id: str, db: Session = Depends(get_db)):
    new_escalation = models.Escalation(name=name, email=email, issue=issue, report_id=report_id)
    db.add(new_escalation)
    db.commit()
    db.refresh(new_escalation)
    return {"status": "success", "id": new_escalation.id}

@app.post("/chatlog/")
def save_chat(role: str, message: str, db: Session = Depends(get_db)):
    log = models.ChatLog(role=role, message=message)
    db.add(log)
    db.commit()
    return {"status": "saved"}
