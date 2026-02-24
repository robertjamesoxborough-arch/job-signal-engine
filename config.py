import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

KEYWORDS = [
    "product",
    "partner",
    "partnership",
    "ecosystem",
    "platform",
    "segment",
    "proposition",
    "growth",
    "commercial",
    "strategy",
    "digital",
    "ai"
]

UK_FILTER_TERMS = [
    "united kingdom",
    "uk",
    "london",
    "manchester",
    "remote - uk",
    "edinburgh",
    "birmingham"
]
