import streamlit as st
import pandas as pd
from db import run_query

def main():
    st.title("📬 Contact Us")

st.sidebar.header("Filter Providers")
city_filter = st.sidebar.text_input("City")
provider_filter = st.sidebar.text_input("Provider Name")

query = "SELECT provider_id, name, type, contact, address, city FROM providers WHERE 1=1"
params = {}
if city_filter:
    query += " AND city ILIKE %(city_filter)s"
    params["city_filter"] = f"%{city_filter}%"
if provider_filter:
    query += " AND name ILIKE %(provider_filter)s"
    params["provider_filter"] = f"%{provider_filter}%"

provider_data = run_query(query, params if params else None)
st.subheader("Provider Contact Details")
st.dataframe(provider_data)

# Contact Form
st.subheader("Send Us a Message")
with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    if st.form_submit_button("Send Message"):
        if name and email and message:
            st.success("✅ Thank you! Your message has been sent.")
            st.info(f"Name: {name}\nEmail: {email}\nMessage: {message}")
        else:
            st.error("❌ Please fill all fields")
