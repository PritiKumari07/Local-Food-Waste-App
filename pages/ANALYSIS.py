import streamlit as st
import pandas as pd
import psycopg2
import altair as alt

st.title("📊 Food Donation Analysis Dashboard")

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="food_data",
        user="postgres",
        password="0719"
    )

conn = get_connection()

# --- 1. Total providers and receivers ---
totals_query = """
SELECT
    (SELECT COUNT(*) FROM providers) AS total_providers,
    (SELECT COUNT(*) FROM receivers) AS total_receivers
"""
totals = pd.read_sql(totals_query, conn)
st.subheader("Total Participants")
st.metric("Providers", totals.total_providers[0])
st.metric("Receivers", totals.total_receivers[0])

# --- 2. Total food listings and quantity ---
food_totals_query = """
SELECT COUNT(*) AS total_listings, SUM(quantity) AS total_quantity
FROM food_listings
"""
food_totals = pd.read_sql(food_totals_query, conn)
st.subheader("Food Listings Overview")
st.metric("Total Listings", food_totals.total_listings[0])
st.metric("Total Quantity", food_totals.total_quantity[0])

# --- 3. Food donated by type (Bar chart) ---
food_type_query = """
SELECT food_type, SUM(quantity) AS total_quantity
FROM food_listings
GROUP BY food_type
ORDER BY total_quantity DESC
"""
food_type_data = pd.read_sql(food_type_query, conn)
st.subheader("Food Donated by Type")
chart = alt.Chart(food_type_data).mark_bar().encode(
    x=alt.X('food_type', sort='-y'),
    y='total_quantity',
    tooltip=['food_type', 'total_quantity']
).properties(width=600, height=400)
st.altair_chart(chart, use_container_width=True)

# --- 4. Top 5 cities by donations (Bar chart) ---
city_query = """
SELECT p.city, COUNT(f.food_id) AS total_donations
FROM food_listings f
JOIN providers p ON f.provider_id = p.provider_id
GROUP BY p.city
ORDER BY total_donations DESC
LIMIT 5
"""
city_data = pd.read_sql(city_query, conn)
st.subheader("Top 5 Cities by Donations")
chart_cities = alt.Chart(city_data).mark_bar(color='orange').encode(
    x=alt.X('city', sort='-y'),
    y='total_donations',
    tooltip=['city', 'total_donations']
).properties(width=600, height=400)
st.altair_chart(chart_cities, use_container_width=True)

# --- 5. Donations trend over time (Line chart) ---
trend_query = """
SELECT DATE(expiry_date) AS date, SUM(quantity) AS total_quantity
FROM food_listings
GROUP BY DATE(expiry_date)
ORDER BY date
"""
trend_data = pd.read_sql(trend_query, conn)
st.subheader("Donations Trend Over Time")
line_chart = alt.Chart(trend_data).mark_line(point=True).encode(
    x='date',
    y='total_quantity',
    tooltip=['date', 'total_quantity']
).properties(width=700, height=400)
st.altair_chart(line_chart, use_container_width=True)

# --- 6. Top 5 donors (Bar chart) ---
top_donors_query = """
SELECT p.name AS provider_name, SUM(f.quantity) AS total_quantity
FROM food_listings f
JOIN providers p ON f.provider_id = p.provider_id
GROUP BY p.name
ORDER BY total_quantity DESC
LIMIT 5
"""
top_donors = pd.read_sql(top_donors_query, conn)
st.subheader("Top 5 Donors")
donors_chart = alt.Chart(top_donors).mark_bar(color='green').encode(
    x=alt.X('provider_name', sort='-y'),
    y='total_quantity',
    tooltip=['provider_name', 'total_quantity']
).properties(width=600, height=400)
st.altair_chart(donors_chart, use_container_width=True)

# --- 7. Top 5 receivers (Bar chart) ---
top_receivers_query = """
SELECT r.name AS receiver_name, COUNT(c.claim_id) AS claims_made
FROM claims c
JOIN receivers r ON c.receiver_id = r.receiver_id
GROUP BY r.name
ORDER BY claims_made DESC
LIMIT 5
"""
top_receivers = pd.read_sql(top_receivers_query, conn)
st.subheader("Top 5 Receivers")
receivers_chart = alt.Chart(top_receivers).mark_bar(color='purple').encode(
    x=alt.X('receiver_name', sort='-y'),
    y='claims_made',
    tooltip=['receiver_name', 'claims_made']
).properties(width=600, height=400)
st.altair_chart(receivers_chart, use_container_width=True)

# --- 8. Food type percentage (Pie chart using Altair) ---
st.subheader("Food Type Distribution")
food_type_data['percentage'] = (food_type_data['total_quantity'] / food_type_data['total_quantity'].sum()) * 100
pie_chart = alt.Chart(food_type_data).mark_arc().encode(
    theta='percentage',
    color='food_type',
    tooltip=['food_type', 'percentage']
)
st.altair_chart(pie_chart, use_container_width=True)

conn.close()
