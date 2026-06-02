import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Page Configuration
st.set_page_config(page_title="Precision Agriculture App", page_icon="🌱", layout="centered")

st.title("🌱 Precision Agriculture: Crop Recommendation System")
st.write("Input the soil properties and weather parameters below to get real-time crop recommendations powered by Machine Learning.")
st.markdown("---")

# 2. Load the Saved Model Artifact
@st.cache_resource
def load_model():
    return joblib.load('crop_model.pkl')

try:
    model = load_model()
except FileNotFoundError:
    st.error("Model file 'crop_model.pkl' not found! Run your Jupyter Notebook pipeline first to generate the file.")

# 3. Interactive User Input UI Components
st.subheader("📊 Enter Soil Metrics & Climate Conditions")

col1, col2 = st.columns(2)

with col1:
    N = st.slider("Nitrogen (N) Content", min_value=0, max_value=150, value=40)
    P = st.slider("Phosphorus (P) Content", min_value=0, max_value=150, value=50)
    K = st.slider("Potassium (K) Content", min_value=0, max_value=210, value=40)
    ph = st.number_input("Soil pH Level (0.0 - 14.0)", min_value=0.0, max_value=14.0, value=6.5, step=0.1)

with col2:
    temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.5)
    humidity = st.slider("Humidity Percentage (%)", min_value=0.0, max_value=100.0, value=70.0)
    rainfall = st.number_input("Annual Rainfall (mm)", min_value=0.0, max_value=400.0, value=100.0, step=10.0)

st.markdown("---")

# 4. Inference Engine Execution
if st.button("🔮 Recommend Optimal Crop"):
    # Format inputs into a NumPy array matching model schema
    input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    
    # Run predictions and extract classification confidence
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)
    confidence = np.max(probabilities) * 100
    
    # Render Output Screens
    st.balloons()
    st.success(f"### 🌾 Recommended Crop for Cultivation: **{prediction.upper()}**")
    
    st.write(f"🤖 Prediction Confidence Score: `{confidence:.2f}%`")
    st.progress(int(confidence))
    
    # Actionable Soil Health Warnings
    if ph < 6.0:
        st.warning("⚠️ Warning: Your soil is acidic. Consider adding agricultural lime to stabilize pH values.")
    elif ph > 7.5:
        st.warning("⚠️ Warning: Your soil is alkaline. Consider adding organic matter or sulfur to lower the pH.")