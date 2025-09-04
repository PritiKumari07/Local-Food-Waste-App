import streamlit as st
import pandas as pd
from db import get_connection

st.title("🍽️ Manage Food Donations")

menu = ["Add Donation", "View Donations", "Update Donation", "Delete Donation"]
choice = st.sidebar.selectbox("Select Operation", menu)

engine = get_connection()

# ---------------- ADD DONATION ----------------
if choice == "Add Donation":
    st.subheader("➕ Add a New Donation")
    food_id = st.number_input("Food ID", min_value=1, step=1)
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
                f"""INSERT INTO food_listings (food_id,food_name,quantity,expiry_date,provider_id, provider_type,location,food_type,meal_type)
                    VALUES (:food_id, :food_name, :quantity, :expiry_date, :provider_id, :provider_type, :location, :food_type, :meal_type)
                """,
                {
                    "food_id": food_id, "food_name": food_name,
                    "quantity": quantity, "expiry_date": expiry_date,
                    "provider_id": provider_id, "provider_type": provider_type,
                    "location": location, "food_type": food_type, "meal_type": meal_type
                }
            )
        st.success("✅ Donation added successfully!")

# ---------------- VIEW DONATIONS ----------------
elif choice == "View Donations":
    st.subheader("📋 All Donations")
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM food_listings ORDER BY food_id ASC", conn)
        st.dataframe(df)

# ---------------- UPDATE DONATION ----------------
elif choice == "Update Donation":
    st.subheader("✏️ Update an Existing Donation")
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM food_listings", conn)

    donation_ids = df["food_id"].tolist()
    selected_id = st.selectbox("Select Donation ID", donation_ids)

    selected_row = df[df["food_id"] == selected_id].iloc[0]

    new_food_name = st.text_input("Food Name", selected_row["food_name"])
    new_food_type = st.text_input("Food Type", selected_row["food_type"])
    new_quantity = st.number_input("Quantity", min_value=1, value=int(selected_row["quantity"]))
    new_expiry_date = st.date_input("Expiry Date", selected_row["expiry_date"])

    if st.button("Update Donation"):
        with engine.begin() as conn:
            conn.execute(
                "UPDATE food_listings SET food_name=:food_name, food_type=:food_type, quantity=:quantity, expiry_date=:expiry_date WHERE food_id=:food_id",
                {
                    "food_name": new_food_name, "food_type": new_food_type,
                    "quantity": new_quantity, "expiry_date": new_expiry_date,
                    "food_id": selected_id,
                }
            )
        st.success(f"✅ Donation ID {selected_id} updated successfully!")

# ---------------- DELETE DONATION ----------------
elif choice == "Delete Donation":
    st.subheader("🗑️ Delete a Donation")
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM food_listings", conn)

    donation_ids = df["food_id"].tolist()
    selected_id = st.selectbox("Select Donation ID to Delete", donation_ids)

    if st.button("Delete Donation"):
        with engine.begin() as conn:
            conn.execute("DELETE FROM food_listings WHERE food_id=:food_id", {"food_id": selected_id})
        st.success(f"✅ Donation ID {selected_id} deleted successfully!")

    st.dataframe(df)
