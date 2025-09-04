import streamlit as st
import psycopg2
from psycopg2.extras import DictCursor
import pandas as pd

def get_connection():
    try:
        return psycopg2.connect(**st.secrets["postgres"])
    except Exception:
        return psycopg2.connect(
            host="localhost",
            user="postgres",
            password="0719",
            database="food_data"
        )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # --- Create tables ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS providers (
        provider_id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        type VARCHAR(100),
        address TEXT,
        city VARCHAR(100),
        contact VARCHAR(50)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receivers (
        receiver_id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        type VARCHAR(100),
        city VARCHAR(100),
        contact VARCHAR(50)
    );
    """)

    cursor.execute("""
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
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS claims (
        claim_id SERIAL PRIMARY KEY,
        food_id INT REFERENCES food_listings(food_id),
        receiver_id INT REFERENCES receivers(receiver_id),
        status VARCHAR(50),
        timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()

    # --- Load data from CSVs ---
    try:
        # Providers
        df_providers = pd.read_csv("data/providers.csv")
        for _, row in df_providers.iterrows():
            cursor.execute("""
                INSERT INTO providers (provider_id, name, type, address, city, contact)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (provider_id) DO NOTHING;
            """, tuple(row))

        # Receivers
        df_receivers = pd.read_csv("data/receivers.csv")
        for _, row in df_receivers.iterrows():
            cursor.execute("""
                INSERT INTO receivers (receiver_id, name, type, city, contact)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (receiver_id) DO NOTHING;
            """, tuple(row))

        # Food Listings
        df_food = pd.read_csv("data/food_listings.csv")
        for _, row in df_food.iterrows():
            cursor.execute("""
                INSERT INTO food_listings (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (food_id) DO NOTHING;
            """, tuple(row))

        # Claims
        df_claims = pd.read_csv("data/claims.csv")
        for _, row in df_claims.iterrows():
            cursor.execute("""
                INSERT INTO claims (claim_id, food_id, receiver_id, status, timestamp)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (claim_id) DO NOTHING;
            """, tuple(row))

    except Exception as e:
        print("Error loading CSV data:", e)

    conn.commit()
    cursor.close()
    conn.close()

# Example function to fetch dashboard data
def fetch_dashboard_data():
    init_db()  # Ensure tables and CSV data exist

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)

    cursor.execute("SELECT COUNT(*) AS meals_saved FROM claims WHERE status = 'Completed';")
    meals_saved = cursor.fetchone()["meals_saved"]

    cursor.execute("SELECT COUNT(DISTINCT provider_id) AS partners FROM providers;")
    partners = cursor.fetchone()["partners"]

    cursor.execute("SELECT COUNT(DISTINCT city) AS cities FROM providers;")
    cities = cursor.fetchone()["cities"]

    cursor.close()
    conn.close()

    return meals_saved, partners, cities
