import streamlit as st
import pandas as pd
from db import get_connection

st.title("📊 SQL Queries and Outputs")

queries = {
        "How many food providers and receivers are there in each city?": """
        SELECT
            city,
            SUM(provider_count) AS provider_count,
            SUM(receiver_count) AS receiver_count
        FROM (
            SELECT city, COUNT(*) AS provider_count, 0 AS receiver_count
            FROM providers
            GROUP BY city
            UNION ALL
            SELECT city, 0 AS provider_count, COUNT(*) AS receiver_count
            FROM receivers
            GROUP BY city
        ) t
        GROUP BY city;
    """,

    "Which type of food provider contributes the most food?": """
        SELECT provider_type, SUM(quantity) AS total_food_quantity
        FROM food_listings
        GROUP BY provider_type
        ORDER BY total_food_quantity DESC;
    """,

    "What is the contact information of food providers in a specific city?": """
        SELECT name, contact, address, city
        FROM providers
        WHERE city = 'Valentineside';
    """,

    "Which receivers have claimed the most food?": """
        SELECT r.name, SUM(f.quantity) AS total_claimed_quantity
        FROM claims c
        JOIN receivers r ON c.receiver_id = r.receiver_id
        JOIN food_listings f ON c.food_id = f.food_id
        WHERE c.status = 'Completed'
        GROUP BY r.name
        ORDER BY total_claimed_quantity DESC;
    """,

    "Total quantity of food available from all providers": """
        SELECT SUM(quantity) AS total_available_quantity
        FROM food_listings;
    """,

    "Which city has the highest number of food listings?": """
        SELECT p.city, COUNT(*) AS listings_count
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.provider_id
        GROUP BY p.city
        ORDER BY listings_count DESC
        LIMIT 1;
    """,

    "Most commonly available food types": """
        SELECT food_type, COUNT(*) AS count_type
        FROM food_listings
        GROUP BY food_type
        ORDER BY count_type DESC;
    """,

    "How many food claims have been made for each food item?": """
        SELECT f.food_name, COUNT(c.claim_id) AS claims_count
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        GROUP BY f.food_name
        ORDER BY claims_count DESC;
    """,

    "Which provider has had the highest number of successful food claims?": """
        SELECT p.name, COUNT(c.claim_id) AS successful_claims
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        JOIN providers p ON f.provider_id = p.provider_id
        WHERE c.status = 'Completed'
        GROUP BY p.name
        ORDER BY successful_claims DESC
        LIMIT 1;
    """,

    "Percentage of claims completed vs pending vs canceled.": """
        SELECT status,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS percentage
        FROM claims
        GROUP BY status;
    """,

    "Average quantity of food claimed per receiver.": """
        SELECT r.name, ROUND(AVG(f.quantity)::numeric, 2) AS avg_quantity_claimed
        FROM claims c
        JOIN receivers r ON c.receiver_id = r.receiver_id
        JOIN food_listings f ON c.food_id = f.food_id
        WHERE c.status = 'Completed'
        GROUP BY r.name;
    """,

    "Which meal type is claimed the most?": """
        SELECT f.food_type, COUNT(c.claim_id) AS claims_count
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        GROUP BY f.food_type
        ORDER BY claims_count DESC
        LIMIT 1;
    """,

    "Total quantity of food donated by each provider": """
        SELECT p.name, SUM(f.quantity) AS total_donated
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.provider_id
        GROUP BY p.name
        ORDER BY total_donated DESC;
    """,

    "Total listed food quantity vs unclaimed food quantity": """
        SELECT
           (SELECT SUM(quantity) FROM food_listings) AS total_food_listed,
           (SELECT SUM(fl.quantity)
            FROM food_listings fl
            LEFT JOIN claims c ON fl.food_id = c.food_id
            WHERE c.claim_id IS NULL
           ) AS total_unclaimed_food;
    """,

    "Which food type is most often claimed but least often completed?": """
        SELECT
            fl.food_type,
            SUM(CASE WHEN c.status = 'Completed' THEN 1 ELSE 0 END) AS completed,
            COUNT(*) AS total_claims,
            (COUNT(*) - SUM(CASE WHEN c.status = 'Completed' THEN 1 ELSE 0 END)) AS incomplete
        FROM claims c
        JOIN food_listings fl ON c.food_id = fl.food_id
        GROUP BY fl.food_type
        ORDER BY incomplete DESC, completed ASC
        LIMIT 1;
    """,

    "Donation activity for the whole week": """
        SELECT
            (EXTRACT(DOW FROM expiry_date)::int + 1) AS weekday,
            SUM(quantity) AS total_quantity_donated
        FROM food_listings
        GROUP BY weekday
        ORDER BY weekday;
    """

}

choice = st.selectbox("🔍 Select a query to run:", list(queries.keys()))

if st.button("Run Query"):
    engine = get_connection()
    with engine.connect() as conn:
        df = pd.read_sql(queries[choice], conn)
        st.write("### Results")
        st.dataframe(df)
