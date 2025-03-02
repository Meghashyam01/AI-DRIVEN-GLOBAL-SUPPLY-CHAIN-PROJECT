import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib  # To save and load the model

# Load the dataset (for training only)
df = pd.read_csv("MILESTONE2/added_transportdelays_with_risk.csv",encoding='latin-1')  # Replace with your dataset file name

# Encode categorical columns (Transport Status and Geopolitical Risk)
label_encoders = {}
categorical_cols = ['Transport Status', 'Geopolitical Risk']
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features (X) and target (y) for training
X = df[['Sentiment Score', 'Transport Status', 'Lead Time (days)', 'Geopolitical Risk', 'route_risk_level']]
y = df['Risk Factor']  # Replace 'Risk Factor' with the actual column name for risk factor

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_scaled, y)

# Save the model and scaler (optional)
joblib.dump(model, 'risk_factor_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

# Load the model and scaler (if saved)
model = joblib.load('risk_factor_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Function to predict risk factor for user input
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

# Get user input at runtime
print("Enter the following details to predict the risk factor:")
sentiment_score = float(input("Sentiment Score (e.g., 0.2): "))
transport_status = input("Transport Status (e.g., Delayed, On Time, In Transit): ")
lead_time = int(input("Lead Time (days) (e.g., 5): "))
geopolitical_risk = input("Geopolitical Risk (e.g., Low, Medium, High): ")
route_risk_level = float(input("Route Risk Level (e.g., 3.5): "))

# Get the predicted risk factor
predicted_risk = predict_risk_factor(sentiment_score, transport_status, lead_time, geopolitical_risk, route_risk_level)
print(f"\nPredicted Risk Factor: {predicted_risk}")