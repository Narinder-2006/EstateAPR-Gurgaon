import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
from config import BASE_DIR
# Page config
st.set_page_config(
    page_title="EstateAPR Gurgaon",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .stat-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .feature-card {
        background: #1e1e1e;
        padding: 2rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        height: 100%;
        color: white;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .insight-card {
        background: #1e1e1e;
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
    .insight-card h4 {
        color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
current_hour = datetime.now().hour
greeting = "Good Morning" if current_hour < 12 else "Good Afternoon" if current_hour < 18 else "Good Evening"

st.markdown(f"""
    <div class="main-header">
        <h1>🏘️ {greeting}! Welcome to EstateAPR Gurgaon </h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            A comprehensive platform for property Analyzation , predictions, and recommendations
        </p>
    </div>
""", unsafe_allow_html=True)

# Quick Stats
st.markdown("### 📊 Latest Update")
st.info(f"🕒 Data last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

st.markdown("<br>", unsafe_allow_html=True)

# Feature Cards
st.markdown("### 🚀 Explore Our Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>📈 Analytics Dashboard</h3>
            <p>Explore comprehensive market insights with interactive visualizations. Analyze price trends, sector comparisons, and property distributions across Gurgaon.</p>
            <ul style="text-align: left; margin-top: 1rem;">
                <li>Interactive sector price maps</li>
                <li>Price vs built-up area analysis</li>
                <li>Bedroom & luxury distribution</li>
                <li>Top sectors by price/sqft</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔍 View Dashboard", key="dash", use_container_width=True):
        st.switch_page(BASE_DIR /'pages'/'DashBoard.py')

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>🎯 Price Prediction</h3>
            <p>Get accurate property price predictions powered by machine learning. Enter your dream house specifications and receive instant price estimates.</p>
            <ul style="text-align: left; margin-top: 1rem;">
                <li>ML-powered predictions</li>
                <li>Multiple property parameters</li>
                <li>Sector-wise analysis</li>
                <li>Instant price estimates</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    if st.button("💰 Predict Price", key="pred", use_container_width=True):
        st.switch_page(BASE_DIR /'pages'/'Price_Prediction.py')

with col3:
    st.markdown("""
        <div class="feature-card">
            <h3>🏡 Recommendations</h3>
            <p>Discover properties tailored to your needs. Find properties near your preferred location with detailed facility information and smart recommendations.</p>
            <ul style="text-align: left; margin-top: 1rem;">
                <li>Location-based search</li>
                <li>Radius filtering</li>
                <li>Facility details</li>
                <li>Similar property suggestions</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔎 Find Properties", key="rec", use_container_width=True):
        st.switch_page(BASE_DIR /'pages'/'Recommendations.py')

st.markdown("<br>", unsafe_allow_html=True)

# Quick Insights Section
st.markdown("### 💡 Quick Market Insights")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class="insight-card">
            <h4>🔥 Trending Sectors</h4>
            <p><strong>Sector 106</strong> - Most properties available</p>
            <p><strong>Sector 82</strong> - Highest price/sqft at ₹30k+</p>
            <p><strong>Sector 27</strong> - Premium luxury segment</p>
            <p style="margin-top: 1rem; color: #667eea;">
                <em>Updated: {datetime.now().strftime("%B %d, %Y")}</em>
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="insight-card">
            <h4>📍 Popular Property Types</h4>
            <p><strong>3 BHK Apartments</strong> - 34.27% of market</p>
            <p><strong>2 BHK Flats</strong> - 25.17% of listings</p>
            <p><strong>4 BHK Luxury</strong> - Growing segment</p>
            <p style="margin-top: 1rem; color: #667eea;">
                <em>Based on 5,834 properties analyzed</em>
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Getting Started Section
st.markdown("### 🎯 Getting Started")
st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                padding: 2rem; border-radius: 10px; border-left: 4px solid #667eea;">
        <h4>New to our platform? Here's how to begin:</h4>
        <ol style="line-height: 2;">
            <li><strong>Explore the Dashboard</strong> - Get familiar with Gurgaon's real estate market trends</li>
            <li><strong>Try Price Prediction</strong> - Input your requirements and see estimated property prices</li>
            <li><strong>Find Recommendations</strong> - Search for properties near your preferred location</li>
            <li><strong>Compare Options</strong> - Use our analytics to make informed decisions</li>
        </ol>
        <p style="margin-top: 1rem;">
            💼 <strong>Pro Tip:</strong> Use the sidebar navigation to switch between different features seamlessly!
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        **📊 Data Sources**
        - Real estate listings
        - Market analysis reports
        - Property databases
    """)

with col2:
    st.markdown("""
        **🔒 Trust & Security**
        - Verified data sources
        - Regular updates
        - Accurate predictions
    """)

with col3:
    st.markdown("""
        **📞 Support**
        - Email: narinderpartapsingh@gmail.com
        - Last Updated: Jan 2026
        - Version 1.0
    """)

st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <p>Made by Narinder Partap Singh for Gurgaon Real Estate Market Analysis</p>
        <p style="font-size: 0.9rem;">© 2026 PropInsight Gurgaon. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)