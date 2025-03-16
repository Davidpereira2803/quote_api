from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import random
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

def load_quotes():
    with open("lux_data.json", "r", encoding="utf-8") as file:
        return json.load(file)

class QuoteRequest(BaseModel):
    text: str
    author: str
    category: str
    meaning: str

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
