import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

def get_connection():
    try:
        # Prefer Streamlit secrets if present
        pg = st.secrets["postgres"]
        db_url = f"postgresql://{pg['user']}:{pg['password']}@{pg['host']}/{pg['database']}"
        return create_engine(db_url)
    except Exception:
        # Fallback for local dev
        return create_engine("postgresql://postgres:0719@localhost/food_data")

def init_db():
    engine = get_connection()
    with engine.begin() as conn:

        # --- Create tables ---
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS providers (
            provider_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            type VARCHAR(100),
            address TEXT,
            city VARCHAR(100),
            contact VARCHAR(50)
        );
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS receivers (
            receiver_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            type VARCHAR(100),
            city VARCHAR(100),
            contact VARCHAR(50)
        );
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS food_listings (
            food_id SERIAL PRIMARY KEY,
            food_name VARCHAR(255),
            quantity INT,
            expiry_date DATE,
            provider_id INT REFERENCES providers(provider_id),
            provider_type VARCHAR(100),
            location VARCHAR(255),
            food_type VARCHAR(100),
            meal_type VARCHAR(100)
        );
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS claims (
            claim_id SERIAL PRIMARY KEY,
            food_id INT REFERENCES food_listings(food_id),
            receiver_id INT REFERENCES receivers(receiver_id),
            status VARCHAR(50),
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
        """))

        # --- Load data from CSVs ---
        try:
            # Providers
            df_providers = pd.read_csv("data/providers.csv")
            df_providers.to_sql('providers', engine, if_exists='append', index=False, method='multi')
            # Receivers
            df_receivers = pd.read_csv("data/receivers.csv")
            df_receivers.to_sql('receivers', engine, if_exists='append', index=False, method='multi')
            # Food Listings
            df_food = pd.read_csv("data/food_listings.csv")
            df_food.to_sql('food_listings', engine, if_exists='append', index=False, method='multi')
            # Claims
            df_claims = pd.read_csv("data/claims.csv")
            df_claims.to_sql('claims', engine, if_exists='append', index=False, method='multi')
        except Exception as e:
            print("Error loading CSV data:", e)

# Example function to fetch dashboard data
def fetch_dashboard_data():
    init_db()  # Ensure tables and CSV data exist

    engine = get_connection()
    with engine.connect() as conn:
        meals_saved = conn.execute(text(
            "SELECT COUNT(*) AS meals_saved FROM claims WHERE status = 'Completed';"
        )).scalar()
        partners = conn.execute(text(
            "SELECT COUNT(DISTINCT provider_id) AS partners FROM providers;"
        )).scalar()
        cities = conn.execute(text(
            "SELECT COUNT(DISTINCT city) AS cities FROM providers;"
        )).scalar()
    return meals_saved, partners, cities
