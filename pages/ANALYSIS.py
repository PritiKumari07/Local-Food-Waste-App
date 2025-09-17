import streamlit as st
import pandas as pd
import altair as alt
from db import run_query


st.title("📊 Food Donation Analysis Dashboard")

# --- Metrics ---
totals = run_query("""
    SELECT (SELECT COUNT(*) FROM providers) AS total_providers,
           (SELECT COUNT(*) FROM receivers) AS total_receivers,
           (SELECT COUNT(*) FROM food_listings) AS total_listings,
           (SELECT COUNT(*) FROM claims WHERE status='Completed') AS total_meals_claimed
""")
st.metric("Providers", int(totals['total_providers'][0]))
st.metric("Receivers", int(totals['total_receivers'][0]))
st.metric("Total Food Listings", int(totals['total_listings'][0]))
st.metric("Meals Claimed", int(totals['total_meals_claimed'][0]))

# --- City Coverage and Listing Distribution ---
city_coverage = run_query("""
    SELECT city, COUNT(*) AS listings_count
    FROM food_listings
    JOIN providers ON food_listings.provider_id = providers.provider_id
    GROUP BY city
    ORDER BY listings_count DESC
""")
st.subheader("Food Listings by City")
bar_chart = alt.Chart(city_coverage).mark_bar().encode(
    x=alt.X('city:N', sort='-y', title='City'),
    y=alt.Y('listings_count:Q', title='Number of Listings'),
    tooltip=['city', 'listings_count']
).properties(width=700, height=400)
st.altair_chart(bar_chart, use_container_width=True)


# --- Provider Type Contribution ---
provider_types = run_query("""
    SELECT provider_type, SUM(quantity) AS total_food_quantity
    FROM food_listings
    GROUP BY provider_type
    ORDER BY total_food_quantity DESC
""")
st.subheader("Food Provided by Provider Type")
provider_bar = alt.Chart(provider_types).mark_bar(color='teal').encode(
    x=alt.X('provider_type:N', sort='-y', title='Provider Type'),
    y=alt.Y('total_food_quantity:Q', title='Total Food Quantity'),
    tooltip=['provider_type', 'total_food_quantity']
).properties(width=700, height=400)
st.altair_chart(provider_bar, use_container_width=True)


# --- Claim Status Breakdown ---
claim_status = run_query("""
    SELECT status,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS percentage
    FROM claims
    GROUP BY status
""")
st.subheader("Claims Status Distribution")
status_pie = alt.Chart(claim_status).mark_arc().encode(
    theta=alt.Theta(field="percentage", type="quantitative"),
    color=alt.Color(field="status", type="nominal"),
    tooltip=['status', 'percentage']
).properties(width=400, height=400)
st.altair_chart(status_pie, use_container_width=False)


# --- Food Types Analysis ---
food_types = run_query("""
    SELECT food_type, COUNT(*) AS count_type
    FROM food_listings
    GROUP BY food_type
    ORDER BY count_type DESC
    LIMIT 10
""")
st.subheader("Top Food Types")
food_type_bar = alt.Chart(food_types).mark_bar(color='orange').encode(
    x=alt.X('food_type:N', sort='-y', title='Food Type'),
    y=alt.Y('count_type:Q', title='Count'),
    tooltip=['food_type', 'count_type']
).properties(width=700, height=400)
st.altair_chart(food_type_bar, use_container_width=True)


# --- Quantity Trends by Weekday ---
weekly_donations = run_query("""
    SELECT
        (EXTRACT(DOW FROM expiry_date)::int + 1) AS weekday,
        SUM(quantity) AS total_quantity_donated
    FROM food_listings
    GROUP BY weekday
    ORDER BY weekday
""")
# Map numeric weekday to names for better readability
weekday_map = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday',
               5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
weekly_donations['weekday_name'] = weekly_donations['weekday'].map(weekday_map)
st.subheader("Donation Activity by Weekday")
line_chart = alt.Chart(weekly_donations).mark_line(point=True).encode(
    x=alt.X('weekday_name:N', title='Weekday', sort=list(weekday_map.values())),
    y=alt.Y('total_quantity_donated:Q', title='Total Quantity Donated'),
    tooltip=['weekday_name', 'total_quantity_donated']
).properties(width=700, height=400)
st.altair_chart(line_chart, use_container_width=True)


# --- Top Receivers by Claimed Quantity ---
top_receivers = run_query("""
    SELECT r.name, SUM(f.quantity) AS total_claimed_quantity
    FROM claims c
    JOIN receivers r ON c.receiver_id = r.receiver_id
    JOIN food_listings f ON c.food_id = f.food_id
    WHERE c.status = 'Completed'
    GROUP BY r.name
    ORDER BY total_claimed_quantity DESC
    LIMIT 10
""")
st.subheader("Top 10 Receivers by Quantity Claimed")
receiver_bar = alt.Chart(top_receivers).mark_bar(color='green').encode(
    x=alt.X('name:N', sort='-y', title='Receiver Name'),
    y=alt.Y('total_claimed_quantity:Q', title='Quantity Claimed'),
    tooltip=['name', 'total_claimed_quantity']
).properties(width=700, height=400)
st.altair_chart(receiver_bar, use_container_width=True)
