import streamlit as st
import psycopg2
import pandas as pd

# Database connection helper
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="food_data",
        user="postgres",
        password="0719"
    )

st.title("🍽️ Manage Food Donations")

menu = ["Add Donation", "View Donations", "Update Donation", "Delete Donation"]
choice = st.sidebar.selectbox("Select Operation", menu)

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
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO food_listings (food_id,food_name,quantity,expiry_date,provider_id, provider_type,location,food_type,meal_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (food_id, food_name,quantity, expiry_date, provider_id, provider_type, location,food_type,meal_type))
        conn.commit()
        cur.close()
        conn.close()
        st.success("✅ Donation added successfully!")

# ---------------- VIEW DONATIONS ----------------
elif choice == "View Donations":
    st.subheader("📋 All Donations")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM food_listings ORDER BY food_id ASC", conn)
    st.dataframe(df)
    conn.close()

# ---------------- UPDATE DONATION ----------------
elif choice == "Update Donation":
    st.subheader("✏️ Update an Existing Donation")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM food_listings", conn)
    conn.close()

    donation_ids = df["food_id"].tolist()
    selected_id = st.selectbox("Select Donation ID", donation_ids)

    selected_row = df[df["food_id"] == selected_id].iloc[0]

    new_food_name = st.text_input("Food Name", selected_row["food_name"])
    new_food_type = st.text_input("Food Type", selected_row["food_type"])
    new_quantity = st.number_input("Quantity", min_value=1, value=int(selected_row["quantity"]))
    new_expiry_date = st.date_input("Expiry Date", selected_row["expiry_date"])

    if st.button("Update Donation"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE food_listings
            SET food_name=%s, food_type=%s, quantity=%s, expiry_date=%s
            WHERE food_id=%s
        """, (new_food_name, new_food_type, new_quantity, new_expiry_date, selected_id))
        conn.commit()
        cur.close()
        conn.close()
        st.success(f"✅ Donation ID {selected_id} updated successfully!")

# ---------------- DELETE DONATION ----------------
elif choice == "Delete Donation":
    st.subheader("🗑️ Delete a Donation")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM food_listings", conn)
    conn.close()

    donation_ids = df["food_id"].tolist()
    selected_id = st.selectbox("Select Donation ID to Delete", donation_ids)

    if st.button("Delete Donation"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM food_listings WHERE food_id=%s", (selected_id,))
        conn.commit()
        cur.close()
        conn.close()
        st.success(f"✅ Donation ID {selected_id} deleted successfully!")
