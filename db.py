import psycopg2
from psycopg2.extras import DictCursor
import pandas as pd
import streamlit as st

def get_connection():
    """
    Returns a connection to the Neon cloud database using SSL.
    """
    return psycopg2.connect(
        "postgresql://neondb_owner:npg_N0TiljpPE5zx@ep-wandering-dream-a1lzhlqa-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    )

def run_query(query, params=None):
    """
    Executes a SQL query and returns results as a Pandas DataFrame.
    """
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn, params=params)
    finally:
        conn.close()
    return df

def fetch_dashboard_data():
    """
    Fetch summary statistics for the dashboard.
    Returns meals_saved, partners, cities.
    """
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute("SELECT COUNT(*) AS meals_saved FROM claims WHERE status = 'Completed';")
        meals_saved = cursor.fetchone()["meals_saved"]

        cursor.execute("SELECT COUNT(DISTINCT provider_id) AS partners FROM providers;")
        partners = cursor.fetchone()["partners"]

        cursor.execute("SELECT COUNT(DISTINCT city) AS cities FROM providers;")
        cities = cursor.fetchone()["cities"]
    finally:
        cursor.close()
        conn.close()
    
    return meals_saved, partners, cities