# db.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Neon database connection URL
NEON_URL = "postgresql+psycopg2://neondb_owner:npg_ILpvZxJ80eKQ@ep-proud-cell-a10f5zkf-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Create engine
@st.cache_resource
def get_engine():
    return create_engine(NEON_URL)

def init_db():
    """Create all required tables if they don’t exist."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS providers (
            provider_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(100),
            address TEXT,
            city VARCHAR(100),
            contact VARCHAR(50)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS receivers (
            receiver_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(100),
            city VARCHAR(100),
            contact VARCHAR(50)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS food_listings (
            food_id SERIAL PRIMARY KEY,
            food_name VARCHAR(255) NOT NULL,
            quantity INT CHECK (quantity >= 0),
            expiry_date DATE,
            provider_id INT REFERENCES providers(provider_id) ON DELETE CASCADE,
            provider_type VARCHAR(100),
            location VARCHAR(255),
            food_type VARCHAR(100),
            meal_type VARCHAR(100)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS claims (
            claim_id SERIAL PRIMARY KEY,
            food_id INT REFERENCES food_listings(food_id) ON DELETE CASCADE,
            receiver_id INT REFERENCES receivers(receiver_id) ON DELETE CASCADE,
            status VARCHAR(50) CHECK (status IN ('Pending', 'Completed', 'Cancelled')),
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
        """))

def fetch_dashboard_data():
    """Return dashboard summary metrics."""
    engine = get_engine()
    with engine.connect() as conn:
        meals_saved = conn.execute(
            text("SELECT COUNT(*) FROM claims WHERE status = 'Completed'")
        ).scalar() or 0

        partners = conn.execute(
            text("SELECT COUNT(DISTINCT provider_id) FROM providers")
        ).scalar() or 0

        cities = conn.execute(
            text("SELECT COUNT(DISTINCT city) FROM providers")
        ).scalar() or 0

    return meals_saved, partners, cities

def import_csv(csv_path: str, table_name: str):
    """Utility to import CSV data into a given table."""
    df = pd.read_csv(csv_path)
    engine = get_engine()
    df.to_sql(table_name, engine, if_exists="append", index=False)
    return f"✅ Imported {len(df)} rows into {table_name}"
