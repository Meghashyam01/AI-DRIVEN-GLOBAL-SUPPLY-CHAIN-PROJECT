import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

# Load the trained model, scaler, and label encoders
model = joblib.load('risk_factor_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Streamlit app title
st.title("Supply Chain Risk Factor Prediction")

# Input fields for user
st.header("Enter the details:")

# Create input fields
sentiment_score = st.number_input("Sentiment Score (e.g., 0.2):", value=0.2)
transport_status = st.selectbox("Transport Status:", ["Delayed", "On Time", "In Transit"])
lead_time = st.number_input("Lead Time (days) (e.g., 5):", value=5)
geopolitical_risk = st.selectbox("Geopolitical Risk:", ["Low", "Medium", "High"])
route_risk_level = st.number_input("Route Risk Level (e.g., 3.5):", value=3.5)

# Function to predict risk factor
def predict_risk_factor(sentiment_score, transport_status, lead_time, geopolitical_risk, route_risk_level):
    # Encode categorical inputs
    transport_status_encoded = label_encoders['Transport Status'].transform([transport_status])[0]
    geopolitical_risk_encoded = label_encoders['Geopolitical Risk'].transform([geopolitical_risk])[0]

    # Create a DataFrame for the input
    input_data = pd.DataFrame({
        'Sentiment Score': [sentiment_score],
        'Transport Status': [transport_status_encoded],
        'Lead Time (days)': [lead_time],
        'Geopolitical Risk': [geopolitical_risk_encoded],
        'route_risk_level': [route_risk_level]
    })

    # Standardize the input
    input_scaled = scaler.transform(input_data)

    # Predict the risk factor
    risk_factor = model.predict(input_scaled)[0]
    return risk_factor

# Predict button
if st.button("Predict Risk Factor"):
    # Get the predicted risk factor
    risk_factor = predict_risk_factor(sentiment_score, transport_status, lead_time, geopolitical_risk, route_risk_level)
    
    # Display the result
    st.success(f"Predicted Risk Factor: **{risk_factor}**")