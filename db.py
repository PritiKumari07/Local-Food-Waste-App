import psycopg2
from psycopg2.extras import DictCursor
import pandas as pd

def get_connection():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="0719",
        database="food_data"
    )

def run_query(query, params=None):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def fetch_dashboard_data():
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
