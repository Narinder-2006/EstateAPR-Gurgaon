import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pickle

# Page configuration
st.set_page_config(
    page_title="Gurgaon Real Estate Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #f8fafc, #eff6ff);
    }
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Sector coordinates mapping
import json

with open("datasets\sector_coordinates.json", "r") as f:
    sector_coordinates = json.load(f)


# Load your data here
# df = pd.read_csv('your_data.csv')

# Sample data for demonstration


    df = pd.read_csv('datasets/concatenated_properties_for analyzation.csv')

# Add coordinates to dataframe
df['lat'] = df['sector'].map(lambda x: sector_coordinates.get(x, {}).get('lat'))
df['lng'] = df['sector'].map(lambda x: sector_coordinates.get(x, {}).get('lng'))

df = df[df['lat'].notna() & df['lng'].notna()]

# Title
st.title("🏠 Gurgaon Real Estate Analytics Dashboard")
st.markdown("### Comprehensive Market Insights and Trends")

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Luxury category filter
luxury_options = ['All'] + list(df['luxury_category'].unique())
selected_luxury = st.sidebar.selectbox("Luxury Category", luxury_options)

# Bedroom filter
bedroom_options = ['All'] + sorted(df['bedRoom'].unique())
selected_bedroom = st.sidebar.selectbox("Bedrooms", bedroom_options)

# Price range filter
price_range = st.sidebar.slider(
    "Price Range (Cr)",
    float(df['price'].min()),
    float(df['price'].max()),
    (float(df['price'].min()), float(df['price'].max()))
)

# Sector filter
sector_options = ['All'] + sorted(df['sector'].unique())
selected_sectors = st.sidebar.multiselect("Sectors", sector_options, default=['All'])

# Apply filters
filtered_df = df.copy()

if selected_luxury != 'All':
    filtered_df = filtered_df[filtered_df['luxury_category'] == selected_luxury]

if selected_bedroom != 'All':
    filtered_df = filtered_df[filtered_df['bedRoom'] == selected_bedroom]

filtered_df = filtered_df[
    (filtered_df['price'] >= price_range[0]) & 
    (filtered_df['price'] <= price_range[1])
]

if 'All' not in selected_sectors and len(selected_sectors) > 0:
    filtered_df = filtered_df[filtered_df['sector'].isin(selected_sectors)]

# KPIs
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
# Meterics
with col1:
    st.metric(
        label="🏘️ Total Properties",
        value=len(filtered_df),
        delta=f"{len(filtered_df) - len(df)} from total"
    )

with col2:
    avg_price = filtered_df['price'].median()
    st.metric(
        label="💰 Median Price",
        value=f"₹{avg_price:.2f} Cr",
        delta=f"{((avg_price/df['price'].median() - 1) * 100):.1f}%"
    )

with col3:
    avg_price_sqft = filtered_df['price_per_sqft'].mean()
    st.metric(
        label="📊 Avg Price/Sqft",
        value=f"₹{avg_price_sqft:,.0f}",
        delta=f"{((avg_price_sqft/df['price_per_sqft'].mean() - 1) * 100):.1f}%"
    )

with col4:
    most_expensive = filtered_df.nlargest(1, 'price_per_sqft')['sector'].values[0] if len(filtered_df) > 0 else "N/A"
    st.metric(
        label="🌟 Top Sector",
        value=most_expensive.title(),
        delta="Most Expensive"
    )

st.markdown("---")

# Geographic Map
st.subheader("🗺️ Interactive Sector Price Map")

# Aggregate data by sector
sector_agg = filtered_df.groupby('sector').agg({
    'price_per_sqft': 'mean',
    'price': 'mean',
    'lat': 'first',
    'lng': 'first'
}).reset_index()

sector_agg['price_per_sqft'] = sector_agg['price_per_sqft'].round(0)
sector_agg['price'] = sector_agg['price'].round(2)

# Create map
fig_map = px.scatter_mapbox(
    sector_agg,
    lat='lat',
    lon='lng',
    size='price',
    color='price_per_sqft',
    hover_name='sector',
    hover_data={
        'price_per_sqft': ':,.0f',
        'price': ':.2f',
        'lat': False,
        'lng': False
    },
    color_continuous_scale='Viridis',
    mapbox_style='open-street-map',
    zoom=10,
    height=600,
    labels={
        'price_per_sqft': 'Price/Sqft (₹)',
        'price': 'Avg Price (Cr)'
    }
)

fig_map.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    coloraxis_colorbar=dict(
        title="₹/Sqft",
        tickformat=",d"
    )
)

st.plotly_chart(fig_map, use_container_width=True)

# Charts section
st.markdown("---")
col1, col2 = st.columns(2)

# Top Sectors by Price/Sqft
with col1:
    st.subheader("📈 Top Sectors by Price/Sqft")
    top_sectors = filtered_df.groupby('sector')['price_per_sqft'].mean().sort_values(ascending=False).head(10)
    
    fig_sectors = go.Figure(data=[
        go.Bar(
            x=top_sectors.values,
            y=top_sectors.index,
            orientation='h',
            marker=dict(
                color=top_sectors.values,
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="₹/Sqft")
            ),
            text=[f"₹{v:,.0f}" for v in top_sectors.values],
            textposition='auto',
        )
    ])
    
    fig_sectors.update_layout(
        xaxis_title="Average Price per Sqft (₹)",
        yaxis_title="Sector",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_sectors, use_container_width=True)

# Bedroom Distribution
with col2:
    st.subheader("🛏️ Bedroom Configuration")
    bedroom_dist = filtered_df['bedRoom'].value_counts().sort_index()
    
    fig_bedroom = go.Figure(data=[
        go.Pie(
            labels=[f"{b} BHK" for b in bedroom_dist.index],
            values=bedroom_dist.values,
            hole=0.4,
            marker=dict(colors=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981'])
        )
    ])
    
    fig_bedroom.update_layout(
        height=400,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5)
    )
    
    st.plotly_chart(fig_bedroom, use_container_width=True)

# Price vs Area
st.subheader("💎 Price vs Built-up Area Analysis")
fig_scatter = px.scatter(
    filtered_df,
    x='built_up_area',
    y='price',
    color='luxury_category',
    size='price_per_sqft',
    hover_data=['sector', 'bedRoom', 'bathroom'],
    color_discrete_map={'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'},
    labels={
        'built_up_area': 'Built-up Area (sqft)',
        'price': 'Price (Cr)',
        'luxury_category': 'Luxury Category'
    },
    height=500
)

fig_scatter.update_traces(marker=dict(line=dict(width=1, color='white')))
fig_scatter.update_layout(
    xaxis_title="Built-up Area (sqft)",
    yaxis_title="Price (₹ Crores)"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# Additional charts
col3, col4 = st.columns(2)

# Luxury Category Distribution
with col3:
    st.subheader("🏆 Luxury Category Distribution")
    luxury_dist = filtered_df['luxury_category'].value_counts()
    
    fig_luxury = go.Figure(data=[
        go.Bar(
            x=luxury_dist.index,
            y=luxury_dist.values,
            marker=dict(
                color=['#10b981', '#f59e0b', '#ef4444'],
                line=dict(color='white', width=2)
            ),
            text=luxury_dist.values,
            textposition='auto',
        )
    ])
    
    fig_luxury.update_layout(
        xaxis_title="Luxury Category",
        yaxis_title="Number of Properties",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_luxury, use_container_width=True)

# Floor Category Impact
with col4:
    st.subheader("🏢 Floor Category Price Impact")
    floor_price = filtered_df.groupby('floor_category')['price'].mean().sort_values()
    
    fig_floor = go.Figure(data=[
        go.Bar(
            x=floor_price.index,
            y=floor_price.values,
            marker=dict(
                color=floor_price.values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Avg Price (Cr)")
            ),
            text=[f"₹{v:.2f} Cr" for v in floor_price.values],
            textposition='auto',
        )
    ])
    
    fig_floor.update_layout(
        xaxis_title="Floor Category",
        yaxis_title="Average Price (₹ Crores)",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_floor, use_container_width=True)

# Price Distribution
st.subheader("📊 Price Distribution Analysis")

fig_dist = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Price Distribution", "Price per Sqft Distribution")
)

# Price histogram
fig_dist.add_trace(
    go.Histogram(
        x=filtered_df['price'],
        nbinsx=30,
        name='Price',
        marker=dict(color='#3b82f6', line=dict(color='white', width=1))
    ),
    row=1, col=1
)

# Price per sqft histogram
fig_dist.add_trace(
    go.Histogram(
        x=filtered_df['price_per_sqft'],
        nbinsx=30,
        name='Price/Sqft',
        marker=dict(color='#8b5cf6', line=dict(color='white', width=1))
    ),
    row=1, col=2
)

fig_dist.update_xaxes(title_text="Price (₹ Crores)", row=1, col=1)
fig_dist.update_xaxes(title_text="Price per Sqft (₹)", row=1, col=2)
fig_dist.update_yaxes(title_text="Frequency", row=1, col=1)
fig_dist.update_yaxes(title_text="Frequency", row=1, col=2)

fig_dist.update_layout(height=400, showlegend=False)
st.plotly_chart(fig_dist, use_container_width=True)

# Amenities Analysis
st.subheader("🎯 Amenities Impact Analysis")

amenities_cols = ['study room', 'servant room', 'store room', 'pooja room']
filtered_df['amenity_score'] = filtered_df[amenities_cols].sum(axis=1)

fig_amenity = px.box(
    filtered_df,
    x='amenity_score',
    y='price',
    color='luxury_category',
    labels={
        'amenity_score': 'Amenity Score',
        'price': 'Price (₹ Crores)',
        'luxury_category': 'Luxury Category'
    },
    height=400
)

st.plotly_chart(fig_amenity, use_container_width=True)

# Age/Possession Analysis
st.subheader("🏗️ Property Age Impact on Pricing")

age_price = filtered_df.groupby('agePossession').agg({
    'price': 'mean',
    'price_per_sqft': 'mean'
}).reset_index()

fig_age = go.Figure()

fig_age.add_trace(go.Bar(
    x=age_price['agePossession'],
    y=age_price['price'],
    name='Avg Price (Cr)',
    marker=dict(color='#3b82f6'),
    yaxis='y',
    offsetgroup=1
))

fig_age.add_trace(go.Bar(
    x=age_price['agePossession'],
    y=age_price['price_per_sqft'],
    name='Avg Price/Sqft',
    marker=dict(color='#f59e0b'),
    yaxis='y2',
    offsetgroup=2
))

fig_age.update_layout(
    xaxis=dict(title="Property Age/Possession"),
    yaxis=dict(title="Average Price (₹ Crores)", side='left'),
    yaxis2=dict(title="Average Price per Sqft (₹)", overlaying='y', side='right'),
    barmode='group',
    height=400,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_age, use_container_width=True)

# Correlation Heatmap
st.subheader("🔥 Feature Correlation Heatmap")

numeric_cols = ['price', 'price_per_sqft', 'bedRoom', 'bathroom', 'built_up_area', 'amenity_score']
correlation_matrix = filtered_df[numeric_cols].corr()

fig_corr = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale='RdBu',
    zmid=0,
    text=correlation_matrix.values.round(2),
    texttemplate='%{text}',
    textfont={"size": 10},
    colorbar=dict(title="Correlation")
))

fig_corr.update_layout(
    height=500,
    xaxis=dict(side='bottom'),
    yaxis=dict(side='left')
)

st.plotly_chart(fig_corr, use_container_width=True)

# Key Insights
st.markdown("---")
st.subheader("💡 Key Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(f"""
    **🏆 Premium Location**  
    {filtered_df.nlargest(1, 'price_per_sqft')['sector'].values[0].title()}  
    ₹{filtered_df['price_per_sqft'].max():,.0f}/sqft
    """)

with col2:
    luxury_premium = filtered_df[filtered_df['luxury_category'] == 'High']['price'].mean() / filtered_df[filtered_df['luxury_category'] == 'Low']['price'].mean() if len(filtered_df[filtered_df['luxury_category'] == 'Low']) > 0 else 0
    st.success(f"""
    **📊 Luxury Premium**  
    {((luxury_premium - 1) * 100):.1f}% higher  
    High vs Low category
    """)

with col3:
    popular_bhk = filtered_df['bedRoom'].mode().values[0] if len(filtered_df) > 0 else 0
    bhk_percent = (filtered_df['bedRoom'].value_counts().values[0] / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.warning(f"""
    **🏠 Popular Choice**  
    {popular_bhk} BHK units  
    {bhk_percent:.1f}% of market
    """)

with col4:
    best_value = filtered_df.nsmallest(1, 'price_per_sqft')['sector'].values[0] if len(filtered_df) > 0 else "N/A"
    st.error(f"""
    **💎 Best Value**  
    {best_value.title()}  
    Competitive pricing
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #64748b;'>
        <p>📊 Dashboard created for Gurgaon Real Estate Market Analysis</p>
        <p>Data updated as of January 2026</p>
        
    </div>
        <div style='text-align: right; color: #64748b;'>
            <p> Created By -</p>
            <p> Narinder Partap Singh </p>
            <p>contact us - narinderpartapsinghasr@gmail.com</p>    </div> 
    """, unsafe_allow_html=True)