from fastapi import FastAPI, Query,  HTTPException
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

def load_quotes(language: str):
    file_map = {
        "lux": "lux_data.json",
        "en": "en_data.json"
    }

    try:
        with open(file_map[language], "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, KeyError):
        raise HTTPException(status_code=400, detail="Invalid language parameter")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error loading quotes data")

class QuoteRequest(BaseModel):
    text: str
    author: str
    category: str
    meaning: str

@app.get("/quotes")
def get_all_quotes(lang: str = Query("lux", regex="^(lux|en)$")):
    quotes = load_quotes(lang)
    return quotes

@app.get("/quote")
def get_random_quote(lang: str = Query("lux", regex="^(lux|en)$")):
    quotes = load_quotes(lang)
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes found")
    return random.choice(quotes)

@app.get("/quotes/category/{category}")
def get_quote_by_category(category: str, lang: str = Query("lux", regex="^(lux|en)$")):
    quotes = [q for q in load_quotes(lang) if q["category"].lower() == category.lower()]
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes found in this category")
    return random.choice(quotes)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
