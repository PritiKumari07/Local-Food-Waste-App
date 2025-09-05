import streamlit as st
from PIL import Image
from pathlib import Path
from db import fetch_dashboard_data, init_db

# Initialize DB on app start
init_db()

# Banner Image
image_path = Path("assets/cover.jpeg")
if image_path.exists():
    st.image(Image.open(image_path), use_container_width=True)
else:
    st.warning("⚠️ Cover image not found. Place it in assets/cover.jpeg")

# Intro
st.markdown("## 🌍 Welcome to Local Food Waste Management App")
st.write("Connecting providers with receivers to reduce food waste.")

# Dashboard
st.subheader("📊 Our Impact So Far")
meals_claimed, partners, cities = fetch_dashboard_data()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Meals Claimed", meals_claimed)
with col2:
    st.metric("Partner Restaurants", partners)
with col3:
    st.metric("Cities Covered", cities)
