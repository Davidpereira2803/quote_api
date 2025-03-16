from fastapi import FastAPI, HTTPException
import json
import random
from pydantic import BaseModel

app = FastAPI()

def load_quotes():
    with open("data.json", "r", encoding="utf-8") as file:
        return json.load(file)

class QuoteRequest(BaseModel):
    text: str
    author: str
    category: str

@app.get("/quotes")
def get_all_quotes():
    quotes = load_quotes()
    return quotes

@app.get("/quote")
def get_random_quote():
    quotes = load_quotes()
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes found")
    return random.choice(quotes)

@app.get("/quotes/category/{category}")
def get_quote_by_category(category: str):
    quotes = [q for q in load_quotes() if q["category"].lower() == category.lower()]
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes found in this category")
    return random.choice(quotes)

@app.post("/quotes")
def add_quote(quote: QuoteRequest):
    quotes = load_quotes()
    new_quote = {
        "id": max(q["id"] for q in quotes) + 1 if quotes else 1,
        "text": quote.text,
        "author": quote.author,
        "category": quote.category
    }
    quotes.append(new_quote)

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=4)

    return {"message": "Quote added successfully", "quote": new_quote}
