from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from pydantic import BaseModel
import random

# Initialize database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for API requests
class QuoteRequest(BaseModel):
    text: str
    author: str
    category: str

# Get a random quote
@app.get("/quote")
def get_random_quote(db: Session = Depends(get_db)):
    quotes = db.query(models.Quote).all()
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes found")
    return random.choice(quotes)

# Get all quotes
@app.get("/quotes")
def get_all_quotes(db: Session = Depends(get_db)):
    return db.query(models.Quote).all()

# Get a quote by category
@app.get("/quotes/category/{category}")
def get_quote_by_category(category: str, db: Session = Depends(get_db)):
    quotes = db.query(models.Quote).filter(models.Quote.category == category).all()
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes found in this category")
    return random.choice(quotes)

# Add a new quote
@app.post("/quotes")
def add_quote(quote: QuoteRequest, db: Session = Depends(get_db)):
    new_quote = models.Quote(text=quote.text, author=quote.author, category=quote.category)
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return {"message": "Quote added successfully", "quote": new_quote}
