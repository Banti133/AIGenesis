import streamlit as st
import folium
from streamlit_folium import folium_static
import random
from dotenv import load_dotenv
import os

load_dotenv('../config/.env')
st.set_page_config(page_title="🌍 Threat Map", layout="wide")

st.title("🌍 Real-Time AI Threat Map")
st.markdown("**Live global visualization of blocked threats** 🚨")

# Sidebar controls
st.sidebar.header("⚙️ Threat Controls")
auto_refresh = st.sidebar.checkbox("Auto-refresh threats", value=True)
risk_level = st.sidebar.slider("Filter by risk", 0, 100, 75)

# Fake threat data (simulates real threats)
threat_types = ["💣 Jailbreak", "🦠 Malware", "🔓 SQL Injection", "🕵️ PII Leak", "🚫 Phishing"]
countries = ["US", "CN", "RU", "IN", "BR", "DE", "FR", "JP", "GB", "CA"]

def generate_threats(n=50):
    threats = []
    for _ in range(n):
        threats.append({
            'lat': random.uniform(-60, 80),
            'lon': random.uniform(-170, 170),
            'country': random.choice(countries),
            'type': random.choice(threat_types),
            'risk': random.randint(20, 100),
            'blocked': random.choice([True, True, True, False])  # 75% blocked
        })
    return threats

# Generate live threats
threats = generate_threats(100)
high_risk_threats = [t for t in threats if t['risk'] >= risk_level]

# Create world map
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")

# Add threat markers
colors = {'💣 Jailbreak': 'red', '🦠 Malware': 'orange', '🔓 SQL Injection': 'yellow', 
          '🕵️ PII Leak': 'purple', '🚫 Phishing': 'pink'}

for threat in high_risk_threats:
    color = colors[threat['type']]
    status = "🛡️ BLOCKED" if threat['blocked'] else "🚨 ACTIVE"
    
    folium.CircleMarker(
        location=[threat['lat'], threat['lon']],
        radius=threat['risk']/10,
        popup=f"""
        <b>{threat['type']}</b><br>
        Country: {threat['country']}<br>
        Risk: {threat['risk']}%<br>
        Status: {status}<br>
        <b>{'✅ SAFE' if threat['blocked'] else '⚠️ DANGER'}</b>
        """,
        color=color,
        fill=True,
        fillOpacity=0.7
    ).add_to(m)

# Stats cards
col1, col2, col3, col4 = st.columns(4)
total_threats = len(threats)
blocked = len([t for t in threats if t['blocked']])
active = total_threats - blocked
high_risk = len(high_risk_threats)

with col1:
    st.metric("Total Threats", total_threats, delta=f"+{random.randint(5,20)}")
with col2:
    st.metric("Blocked", f"{blocked}", delta=f"+{random.randint(2,10)}")
with col3:
    st.metric("Active", active, delta=None)
with col4:
    st.metric("High Risk", high_risk)

# Live map
st.subheader("🌐 Global Threat Heatmap")
folium_static(m, width=1200, height=600)

# Threat list
st.subheader("📊 Recent Threats")
recent = sorted(threats[-10:], key=lambda x: x['risk'], reverse=True)
for threat in recent:
    status_emoji = "🛡️" if threat['blocked'] else "🚨"
    st.write(f"{status_emoji} **{threat['type']}** | {threat['country']} | {threat['risk']}% risk")

# Auto-refresh
if auto_refresh:
    st.balloons()
    st.experimental_rerun()
