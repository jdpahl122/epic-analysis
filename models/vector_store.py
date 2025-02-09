import os
import numpy as np
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import json

# ✅ Load environment variables
load_dotenv()

# ✅ Database Connection
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

# ✅ Load Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text):
    """Generate a vector embedding."""
    return model.encode(text).tolist()

def check_if_epic_exists(epic_id):
    """Check if an epic has already been processed."""
    with SessionLocal() as session:
        result = session.execute(
            text("SELECT COUNT(*) FROM epics WHERE epic_id = :epic_id"),
            {"epic_id": str(epic_id)}
        )
        return result.scalar() > 0

def store_epic(epic):
    """Store an epic's details, embeddings, and related issues."""
    epic_id = epic["epic_id"]

    if check_if_epic_exists(epic_id):
        print(f"⚠️ Epic {epic_id} already stored. Skipping.")
        return

    # Ensure required fields are not None (avoid NULL constraint violations)
    epic_name = epic["name"] if epic["name"] else "Unnamed Epic"
    epic_summary = epic["summary"] if epic["summary"] else "No Summary Available"
    epic_description = str(epic["description"]) if epic["description"] else "No Description Available"

    # Combine fields for embedding
    epic_text = f"Name: {epic_name}\nSummary: {epic_summary}\nDescription: {epic_description}"

    # Generate vector embeddings
    epic_embedding = np.array(embed_text(epic_text))

    with SessionLocal() as session:
        session.execute(
            text("""
                INSERT INTO epics (epic_id, key, name, summary, description, embedding, issues, text)
                VALUES (:epic_id, :key, :name, :summary, :description, :embedding, :issues, :text)
            """),
            {
                "epic_id": epic_id,
                "key": epic["key"],
                "name": epic_name,  # ✅ Ensured not NULL
                "summary": epic_summary,  # ✅ Ensured not NULL
                "description": epic_description,  # ✅ Ensured not NULL
                "embedding": epic_embedding.tolist(),  # ✅ Stored as vector
                "issues": json.dumps(epic["issues"]),  # ✅ Stored as JSONB
                "text": epic_text  # ✅ Ensured `text` column is filled
            }
        )
        session.commit()

    print(f"✅ Stored epic {epic_id} with {len(epic['issues'])} issues and vector embeddings.")
