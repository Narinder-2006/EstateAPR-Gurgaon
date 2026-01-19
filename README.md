# Estate APR Gurugram 🏙️  
### Gurgaon Flats Price Prediction & Recommendation System

## 📌 Project Overview
Estate APR Gurugram is an end-to-end real estate analytics application built on a dataset of approximately **6,000 flats in Gurugram**.  
The project covers the complete data science lifecycle — from **web scraping and data cleaning** to **machine learning-based price prediction**, **recommendation systems**, and an **interactive Streamlit dashboard**.

The application is designed to help users:
- Analyze flat prices in Gurugram
- Predict prices based on input features
- Get flat recommendations using similarity-based matching

---

## 🔄 Project Workflow
1. Web Scraping of real estate listings  
2. Data Cleaning & Preprocessing  
3. Exploratory Data Analysis (EDA)  
4. Feature Engineering
5. Feature Selection
6. Model Training & Evaluation  
7. Recommendation System using Cosine Similarity  
8. Streamlit Web Application Deployment  

> Note: Only the `Streamlit/` folder is required to run the application.  
> The `data_processing/` folder documents the complete development pipeline.

---

## 📂 Project Structure

- Estate APR Gurugram/
- │
- ├── data_processing/
- │ ├── notebooks/
- │ ├── datasets/ 
- │  
- ├── Streamlit/
- │ ├── datasets/
- │ │ ├── concatinated_flats_data_for _analyzation.csv
- | | ├── properties _data.csv
- | | ├── location_data.csv
- │ │ ├── sector_cordinates.json
- │ ├── models/
- │ │ ├── price_prediction_model.pkl
- │ │ ├── cosine_similarity1.pkl
- | | |── cosine_similarity2.pkl
- │ │ └── cosine_similarity3.pkl
- │ │
- │ ├── pages/
- │ │ ├── dashboard.py
- │ │ ├── recommendation.py
- │ │ └── price_prediction.py
- │ │
- │ └── home.py
- │
- ├── requirements.txt
- └── README.md


---

## 🚀 How to Run the Application

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
2️⃣ Navigate to Streamlit folder
cd Streamlit
3️⃣ Run the app
streamlit run home.py
📊 Features
Interactive Dashboard

Price distribution

Area-wise and BHK-wise analysis

Price Prediction

ML-based prediction using trained regression models

Recommendation System

Cosine similarity-based flat recommendations

🛠️ Tech Stack
Python

Pandas, NumPy

Scikit-learn

Plotly

Streamlit

Pickle (model serialization)

👨‍💻 Author
Narinder Partap Singh
B.Tech CSE | Data Science Enthusiast
NIT Jalandhar


---

