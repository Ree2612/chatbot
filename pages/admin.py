import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

st.set_page_config(page_title="Admin Log Panel", layout="wide")

st.title("🛡️ Threat Log Admin Panel")

# CSV column headers (since your file has no header row)
columns = [
    "timestamp", "ip", "city", "region", "country", "countryCode",
    "lat", "lon", "isp", "query", "threat", "terms"
]

# Load logs
try:
    df = pd.read_csv("logs.csv", header=None, names=columns)

    if not df.empty:
        st.subheader("📋 Log Table")
        st.dataframe(df, use_container_width=True)

        # ✅ Convert 'threat' column to string for consistency
        df["threat"] = df["threat"].astype(str)

        # 🔥 Threat Frequency Bar Chart
        st.subheader("⚠️ Threat Frequency")
        threat_df = df[df["threat"] == "True"]
        if not threat_df.empty:
            chart_data = threat_df["terms"].value_counts()
            st.bar_chart(chart_data)
        else:
            st.info("No threats detected yet.")

        # 🌍 Threat Location Map
        st.subheader("🗺️ Threat Locations")
        m = folium.Map(location=[20.59, 78.96], zoom_start=2)

        for _, row in df.iterrows():
            if not pd.isna(row["lat"]) and not pd.isna(row["lon"]):
                icon_color = "red" if row["threat"] == "True" else "green"
                folium.Marker(
                    location=[float(row["lat"]), float(row["lon"])],
                    popup=folium.Popup(
                        f"<b>IP:</b> {row['ip']}<br>"
                        f"<b>City:</b> {row['city']}<br>"
                        f"<b>Country:</b> {row['country']}<br>"
                        f"<b>Query:</b> {row['query']}<br>"
                        f"<b>Threat:</b> {row['terms'] or 'None'}",
                        max_width=300
                    ),
                    icon=folium.Icon(color=icon_color)
                ).add_to(m)

        st_folium(m, width=900, height=500)

        # 🧹 Clear Logs Button
        if st.button("🗑️ Clear Logs"):
            open("logs.csv", "w").close()
            st.success("Logs cleared!")

    else:
        st.info("🕵️ No logs recorded yet.")

except FileNotFoundError:
    st.warning("❌ Log file not found. Try generating logs by chatting with the bot.")
