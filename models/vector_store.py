import os
import numpy as np
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Load DB connection
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text):
    """Generate a vector embedding."""
    return model.encode(text).tolist()

def check_if_epic_exists(epic_id):
    """Check if an epic has already been processed (forcing epic_id to string)."""
    with SessionLocal() as session:
        result = session.execute(
            text("SELECT COUNT(*) FROM epics WHERE epic_id = :epic_id"),
            {"epic_id": str(epic_id)}  # ✅ Convert to string
        )
        return result.scalar() > 0  # Returns True if epic exists

def store_epic(epic_id, epic_text):
    """Store a new epic if it hasn't been stored yet."""
    if check_if_epic_exists(epic_id):
        print(f"⚠️ Epic {epic_id} already stored. Skipping.")
        return

    vector = embed_text(epic_text)
    
    with SessionLocal() as session:
        session.execute(
            text("INSERT INTO epics (epic_id, text, embedding) VALUES (:epic_id, :text, :embedding)"),
            {"epic_id": epic_id, "text": epic_text, "embedding": np.array(vector).tolist()},
        )
        session.commit()

    print(f"✅ Stored new epic {epic_id}.")
