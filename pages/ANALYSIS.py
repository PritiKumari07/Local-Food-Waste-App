import streamlit as st
import pandas as pd
import altair as alt
from db import get_engine

st.title("📊 Food Donation Analysis Dashboard")

engine = get_engine()

try:
    with engine.connect() as conn:
        # Example: totals
        totals = pd.read_sql("""
            SELECT (SELECT COUNT(*) FROM providers) AS total_providers,
                   (SELECT COUNT(*) FROM receivers) AS total_receivers
        """, conn)

        st.metric("Providers", int(totals.total_providers[0]))
        st.metric("Receivers", int(totals.total_receivers[0]))

        # Same queries as before …
        # (Your existing chart code is fine, just replace engine usage with get_engine)
except Exception as e:
    st.error(f"❌ Could not fetch data: {e}")
