import streamlit as st
from PIL import Image
import psycopg2
from db import fetch_dashboard_data

# Page Config

st.set_page_config(page_title="Local Food Waste Management System", layout="wide")



cover_image = Image.open("/Users/pritidwivedi/Downloads/cover.jpeg")
st.image(cover_image, use_container_width=True)

    ## 🌱 **Sustainability**:

st.markdown("""
                <div style="text-align: center;">

            ## 🌎 Environmental Impact:
              Food waste contributes significantly to 8-10% of global greenhouse gas emissions.<br>
              Managing food waste locally helps reduce methane emissions and air pollution.<br>
              It minimizes the carbon footprint from transporting excess food.<br>
              Better utilization of food conserves water, soil, and energy used in production.<br>
              Effective waste management protects ecosystems and supports sustainability.


            ## 🏠 Community Benefits:
             Strengthens local food systems by redistributing surplus food.<br>
             Supports food banks and community organizations.<br>
             Encourages collaboration among local businesses, nonprofits, and government agencies.<br>
             Helps communities build resilience against food insecurity.<br>
             Promotes a sense of unity and shared responsibility.


            ## 💰 Economic Savings:
             Reducing food waste saves money for households and businesses.<br>
             Businesses lower disposal costs while gaining tax benefits from donations.<br>
             Families save by cutting unnecessary purchases.<br>
             Efficient use of food lowers overall operational costs for suppliers.<br>
             Donations turn waste into valuable community resources.


            ## 🤝 Social Impact:
             Addresses food insecurity by ensuring surplus food reaches those in need.<br>
             Promotes social equity by distributing resources fairly.<br>
             Strengthens community connections through collaboration.<br>
             Builds a culture of sharing and responsibility.<br>
             Creates a positive community identity around sustainability.

            </div>""", unsafe_allow_html=True)

            # --- Dashboard Section ---
st.subheader("Our Impact So Far")

meals_claimed, partners, cities = fetch_dashboard_data()


st.markdown(
                f"""
                <div style="background-color:#4CAF50;padding:30px;border-radius:10px;text-align:center;">
                    <h2 style="color:white;">{meals_claimed:,}</h2>
                    <p style="color:white;">Meals Claimed</p>
                </div>
                """,
                unsafe_allow_html=True
            )

st.write("") 

            
st.markdown(
                f"""
                <div style="background-color:#2196F3;padding:30px;border-radius:10px;text-align:center;">
                    <h2 style="color:white;">{partners}</h2>
                    <p style="color:white;">Partner Restaurants</p>
                </div>
                """,
                unsafe_allow_html=True
            )

st.write("")

            
st.markdown(
                f"""
                <div style="background-color:#9C27B0;padding:30px;border-radius:10px;text-align:center;">
                    <h2 style="color:white;">{cities}</h2>
                    <p style="color:white;">Cities Covered</p>
                </div>
                """,
                unsafe_allow_html=True
            )


