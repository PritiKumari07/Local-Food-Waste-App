import streamlit as st
from db import get_connection, run_query

def main():
    st.title("🍽️ Manage Food Donations")

menu = ["Add Donation", "View Donations", "Update Donation", "Delete Donation"]
choice = st.sidebar.selectbox("Select Operation", menu)

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
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO food_listings
            (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type),
        )
        conn.commit()
        cursor.close()
        conn.close()
        st.success("✅ Donation added successfully!")


