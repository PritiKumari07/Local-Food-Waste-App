import streamlit as st
import pandas as pd
from db import get_connection

st.title("📬 Contact Us")

st.sidebar.header("Filter Providers")
city_filter = st.sidebar.text_input("City (leave blank for all)")
provider_filter = st.sidebar.text_input("Provider Name (leave blank for all)")

engine = get_connection()

query = "SELECT provider_id, name, type, contact, address, city FROM providers WHERE 1=1"

if city_filter:
    query += f" AND city ILIKE '%{city_filter}%'"
if provider_filter:
    query += f" AND name ILIKE '%{provider_filter}%'"

with engine.connect() as conn:
    provider_data = pd.read_sql(query, conn)
    st.subheader("Provider Contact Details")
    st.dataframe(provider_data)

st.subheader("Send Us a Message")
with st.form(key='contact_form'):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    submit_button = st.form_submit_button(label='Send Message')

    if submit_button:
        if name and email and message:
            st.success("Thank you! Your message has been sent.")
            st.info(f"Name: {name}\nEmail: {email}\nMessage: {message}")
        else:
            st.error("Please fill out all fields before submitting.")
