from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS (so frontend can access this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/patients")
def register_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)
