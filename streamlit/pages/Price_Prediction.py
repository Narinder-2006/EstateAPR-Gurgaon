import streamlit as st
import pandas as pd
import pickle
import numpy as np
import time
from config import BASE_DIR
st.set_page_config(
    page_title="Predict Property Price",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.title("🏡 Property Price Prediction")
st.markdown("---")

col1, col2 = st.columns([1.4, 0.9])  # left wider, right narrower

with col1:
    st.markdown(
        """
        <div style="padding-left:0px; padding-top:60px;padding-bottom:20px;">
            <h1>Lets Predict Price Of Your Dream House</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown('<div style="padding-right:20px;padding-bottom:20px;">', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="margin-top:40px;">
        """,
        unsafe_allow_html=True
    )
    st.image("https://cdn.shopify.com/s/files/1/0278/7289/files/final_without_overlay_1024x1024.png?v=1518448244", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with open("streamlit\models\df.pkl", "rb") as file:
    df = pickle.load(file)
st.markdown("---")
st.subheader("Enter House Details")

# property type
property_type = st.selectbox("Property Type", df["property_type"].unique())
#sector
sector=st.selectbox("Sector",sorted(df['sector'].unique()))
#age of property
age_possession= st.selectbox("Age", df["agePossession"].unique())
# furnishing type
furnishing=st.selectbox("Furnishing type", df["furnishing_type"].unique())
#luxury_cat
luxury=st.selectbox("Luxury type", df["luxury_category"].unique())
#floor
floor=st.selectbox("Floor type", df["floor_category"].unique())
#bALCONY
bal=st.selectbox("Balconies", df["balcony"].unique())
#

bedroom = st.number_input("Bedrooms", min_value=0,max_value=15, step=1)
bathroom = st.number_input("Bathrooms", min_value=0, step=1)
area=st.number_input("Built-up Area (sqft)", min_value=500)
servant=st.number_input("Servant room", max_value=1,min_value=0)
store=st.number_input("Store room", max_value=1,min_value=0)

st.markdown("""
<style>
div.stButton > button {
    background: linear-gradient(90deg, #ff6a00, #ee0979);
    color: white;
    font-size: 18px;
    font-weight: 600;
    padding: 10px 28px;
    border-radius: 10px;
    border: none;
    width: 100%;
}
div.stButton > button:hover {
    background: linear-gradient(30deg, #ee0979, #ff6a00);
}
</style>
""", unsafe_allow_html=True)

button = st.button("🔮 Predict Price")

if button:
    input_df = pd.DataFrame([{
        "property_type": property_type,
        "sector": sector,
        "bedRoom": bedroom,
        "bathroom": bathroom,
        "balcony": bal,
        "agePossession": age_possession,
        "built_up_area": area,
        "servant room": servant,
        "store room": store,
        "furnishing_type": furnishing,
        "luxury_category": luxury,
        "floor_category": floor
    }])

    st.dataframe(input_df,width='content')
    
    with st.spinner("🔍 Calculating house price..."):
        time.sleep(1) 
        with open(BASE_DIR /"models"/"lightgbm_price_pipeline.pkl", "rb") as file:
            model = pickle.load(file)

        prediction = model.predict(input_df)[0]
        prediction = np.expm1(prediction)
        prediction_left=prediction - 0.1*prediction
        prediction_right=prediction + 0.1*prediction

    st.success("✅ Prediction completed!")
    st.subheader(f"💰 Predicted Price is between  {prediction_left:,.2f} Cr and {prediction_right:,.2f} Cr")