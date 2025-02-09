import os
import numpy as np
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from sentence_transformers import SentenceTransformer

load_dotenv()
# Load environment variables
DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/epic_db")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_text(text):
    """Generate a vector embedding for a given text."""
    return model.encode(text).tolist()

def store_epic(epic_id, epic_text):
    """Store an epic's text and embedding in PostgreSQL."""
    vector = embed_text(epic_text)
    
    with SessionLocal() as session:
        session.execute(
            text("INSERT INTO epics (epic_id, text, embedding) VALUES (:epic_id, :text, :embedding) ON CONFLICT (epic_id) DO NOTHING"),
            {"epic_id": epic_id, "text": epic_text, "embedding": np.array(vector).tolist()},
        )
        session.commit()

def query_similar_epics(epic_text, top_k=5):
    """Find the most similar epics based on vector similarity."""
    vector = embed_text(epic_text)
    
    with SessionLocal() as session:
        result = session.execute(
            text(
                "SELECT epic_id, text FROM epics ORDER BY embedding <-> :vector LIMIT :top_k"
            ),
            {"vector": np.array(vector).tolist(), "top_k": top_k},
        )
        return result.fetchall()
