import psycopg2
from psycopg2.extras import DictCursor
import pandas as pd


DB_HOST = "ep-proud-cell-a10f5zkf-pooler.ap-southeast-1.aws.neon.tech"
DB_NAME = "neondb?sslmode=require&channel_binding=require"
DB_USER = "neondb_owner"        
DB_PASSWORD = "npg_ILpvZxJ80eKQ"  
DB_PORT = ""                 

def get_connection():
    """Create a connection to the hosted PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"❌ Error connecting to the database: {e}")
        return None

def run_query(query, params=None):
    """Run a query and return a pandas DataFrame."""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()  
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def fetch_dashboard_data():
    """Fetch key stats for dashboard cards."""
    conn = get_connection()
    if conn is None:
        return 0, 0, 0 

    cursor = conn.cursor(cursor_factory=DictCursor)

    # Meals saved
    cursor.execute("SELECT COUNT(*) AS meals_saved FROM claims WHERE status = 'Completed';")
    meals_saved = cursor.fetchone()["meals_saved"]

    # Partners
    cursor.execute("SELECT COUNT(DISTINCT provider_id) AS partners FROM providers;")
    partners = cursor.fetchone()["partners"]

    # Cities
    cursor.execute("SELECT COUNT(DISTINCT city) AS cities FROM providers;")
    cities = cursor.fetchone()["cities"]

    cursor.close()
    conn.close()
    return meals_saved, partners, cities