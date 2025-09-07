import streamlit as st
import pandas as pd
from db import get_connection


# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(page_title="🍽️ Manage Food Donations", layout="wide")
st.title("🍽️ Manage Food Donations")

menu = ["Add Donation", "View Donations", "Update Donation", "Delete Donation"]
choice = st.sidebar.selectbox("Select Operation", menu)


# ------------------ ADD DONATION ------------------ #
if choice == "Add Donation":
    st.subheader("➕ Add a New Donation")

    food_id = st.number_input("Food ID (Enter manually)", min_value=1, step=1)
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
            (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type),
        )
        conn.commit()
        cursor.close()
        conn.close()
        st.success(f"✅ Donation with Food ID {food_id} added successfully!")


# ------------------ VIEW DONATIONS ------------------ #
elif choice == "View Donations":
    st.subheader("📋 View All Donations")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM food_listings", conn)
    conn.close()

    st.dataframe(df)


# ------------------ UPDATE DONATION ------------------ #
elif choice == "Update Donation":
    st.subheader("✏️ Update Donation Details")

    food_id = st.number_input("Enter Food ID to Update", min_value=1, step=1)
    food_name = st.text_input("New Food Name")
    quantity = st.number_input("New Quantity", min_value=1, step=1)
    expiry_date = st.date_input("New Expiry Date")
    provider_id = st.number_input("New Provider ID", min_value=1, step=1)
    provider_type = st.text_input("New Provider Type")
    location = st.text_input("New Location")
    food_type = st.text_input("New Food Type")
    meal_type = st.text_input("New Meal Type")

    if st.button("Update Donation"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE food_listings
            SET food_name=%s, quantity=%s, expiry_date=%s,
                provider_id=%s, provider_type=%s, location=%s,
                food_type=%s, meal_type=%s
            WHERE food_id=%s
            """,
            (food_name, quantity, expiry_date, provider_id, provider_type,
             location, food_type, meal_type, food_id),
        )
        conn.commit()
        cursor.close()
        conn.close()
        st.success(f"✅ Donation with Food ID {food_id} updated successfully!")


# ------------------ DELETE DONATION ------------------ #
elif choice == "Delete Donation":
    st.subheader("🗑️ Delete a Donation")

    food_id = st.number_input("Enter Food ID to Delete", min_value=1, step=1)

    if st.button("Delete Donation"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM food_listings WHERE food_id=%s", (food_id,))
        conn.commit()
        cursor.close()
        conn.close()
        st.success(f"✅ Donation with Food ID {food_id} deleted successfully!")
