import streamlit as st
import pandas as pd
from db import get_engine

st.title("🍽️ Manage Food Donations")

menu = ["Add Donation", "View Donations", "Update Donation", "Delete Donation"]
choice = st.sidebar.selectbox("Select Operation", menu)

engine = get_engine()

# ---------------- ADD DONATION ----------------
if choice == "Add Donation":
    st.subheader("➕ Add a New Donation")
    food_name = st.text_input("Food Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    expiry_date = st.date_input("Expiry Date")
    provider_id = st.number_input("Provider ID", min_value=1, step=1)
    provider_type = st.text_input("Provider Type")
    location = st.text_input("Location")
    food_type = st.text_input("Food Type")
    meal_type = st.text_input("Meal Type")

    if st.button("Add Donation"):
        with engine.begin() as conn:
            conn.execute(
                """
                INSERT INTO food_listings
                (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
                VALUES (:food_name, :quantity, :expiry_date, :provider_id, :provider_type, :location, :food_type, :meal_type)
                """,
                {
                    "food_name": food_name,
                    "quantity": quantity,
                    "expiry_date": expiry_date,
                    "provider_id": provider_id,
                    "provider_type": provider_type,
                    "location": location,
                    "food_type": food_type,
                    "meal_type": meal_type,
                },
            )
        st.success("✅ Donation added successfully!")
