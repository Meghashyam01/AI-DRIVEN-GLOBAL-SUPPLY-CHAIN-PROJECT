import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt

# Load the trained model, scaler, and label encoders
model = joblib.load('risk_factor_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Initialize inventory for sugar
inventory = {
    "sugar": {
        "capacity": 10000,        # Maximum capacity (in kg)
        "current_stock": 5000,    # Current stock level (in kg)
        "monthly_purchase": 2000, # Monthly incoming stock (in kg)
        "monthly_sales": 2500,    # Monthly outgoing stock (in kg)
        "minimum_stock": 1000,    # Minimum stock threshold (in kg)
        "damaged_stock": 0,       # Stock lost due to damage (in kg)
        "transport_delay": False, # Flag for transport delay
    }
}

# Streamlit app title
st.title("Sugar Supply Chain Management System")

# Sidebar for navigation
st.sidebar.header("Navigation")
options = st.sidebar.radio("Choose an option:", [
    "Predict Risk Factor", "Update Inventory", "Log Damaged Stock", 
    "Log Transport Delay", "View Inventory Status"
])

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

# Function to update inventory
def update_inventory(product, new_stock):
    if product in inventory:
        inventory[product]["current_stock"] += new_stock
        current_stock = inventory[product]["current_stock"]
        minimum_stock = inventory[product]["minimum_stock"]
        capacity = inventory[product]["capacity"]

        st.success(f"Inventory updated for {product}. Current stock: {current_stock} kg")

        # Alerts based on stock levels
        if current_stock < minimum_stock:
            st.warning(f"ALERT: Current stock ({current_stock} kg) is below the minimum threshold ({minimum_stock} kg). Restock immediately!")
        elif current_stock > capacity:
            st.warning(f"WARNING: Current stock ({current_stock} kg) exceeds capacity ({capacity} kg). Consider reducing stock.")
        else:
            st.info("INFO: Stock levels are within a healthy range.")

# Function to log damaged stock
def log_damage(product, damaged_quantity):
    if product in inventory:
        inventory[product]["damaged_stock"] += damaged_quantity
        inventory[product]["current_stock"] -= damaged_quantity
        st.success(f"Damaged stock logged for {product}. Updated current stock: {inventory[product]['current_stock']} kg")
        if inventory[product]["current_stock"] < inventory[product]["minimum_stock"]:
            st.warning(f"ALERT: Current stock is below the minimum threshold ({inventory[product]['minimum_stock']} kg). Restock immediately!")
    else:
        st.error("Error: Product not found.")

# Function to log transport delay
def log_transport_delay(product, delay_days):
    if product in inventory:
        inventory[product]["transport_delay"] = True
        st.warning(f"Transport delay logged for {product}. Delay duration: {delay_days} days")
        st.warning("WARNING: Transport delay will affect inventory replenishment.")
    else:
        st.error("Error: Product not found.")

# Function to view inventory status
def view_inventory():
    st.subheader("Current Inventory Status")
    for product, details in inventory.items():
        st.write(f"**Product:** {product}")
        st.write(f"- Capacity: {details['capacity']} kg")
        st.write(f"- Current Stock: {details['current_stock']} kg")
        st.write(f"- Monthly Purchase: {details['monthly_purchase']} kg")
        st.write(f"- Monthly Sales: {details['monthly_sales']} kg")
        st.write(f"- Minimum Stock: {details['minimum_stock']} kg")
        st.write(f"- Damaged Stock: {details['damaged_stock']} kg")
        st.write(f"- Transport Delay: {'Yes' if details['transport_delay'] else 'No'}")

        # Stock level alerts
        if details["current_stock"] < details["minimum_stock"]:
            st.warning(f"ALERT: Stock critically low for {product}! Restock immediately.")
        elif details["current_stock"] > details["capacity"]:
            st.warning(f"WARNING: Stock exceeds capacity for {product}. Reduce inventory.")
        else:
            st.info(f"INFO: Stock levels for {product} are healthy.")

# Function to plot inventory status
def plot_inventory_status():
    products = list(inventory.keys())
    current_stocks = [inventory[product]["current_stock"] for product in products]
    capacities = [inventory[product]["capacity"] for product in products]
    minimum_stocks = [inventory[product]["minimum_stock"] for product in products]

    fig, ax = plt.subplots()
    x = range(len(products))
    ax.bar(x, current_stocks, width=0.4, label="Current Stock", color='blue')
    ax.bar(x, capacities, width=0.4, label="Capacity", color='green', alpha=0.6, bottom=current_stocks)
    ax.bar(x, minimum_stocks, width=0.4, label="Minimum Stock", color='red', alpha=0.7)

    ax.set_xlabel("Products")
    ax.set_ylabel("Stock Levels (kg)")
    ax.set_title("Inventory Status")
    ax.set_xticks(x)
    ax.set_xticklabels(products)
    ax.legend()
    st.pyplot(fig)

# Main app logic based on user selection
if options == "Predict Risk Factor":
    st.header("Predict Risk Factor")
    sentiment_score = st.number_input("Sentiment Score (e.g., 0.2):", value=0.2)
    transport_status = st.selectbox("Transport Status:", ["Delayed", "On Time", "In Transit"])
    lead_time = st.number_input("Lead Time (days) (e.g., 5):", value=5)
    geopolitical_risk = st.selectbox("Geopolitical Risk:", ["Low", "Medium", "High"])
    route_risk_level = st.number_input("Route Risk Level (e.g., 3.5):", value=3.5)

    if st.button("Predict Risk Factor"):
        risk_factor = predict_risk_factor(sentiment_score, transport_status, lead_time, geopolitical_risk, route_risk_level)
        st.success(f"Predicted Risk Factor: **{risk_factor}**")

elif options == "Update Inventory":
    st.header("Update Inventory")
    product = st.selectbox("Product:", list(inventory.keys()))
    new_stock = st.number_input("New Stock (kg):", value=0)
    if st.button("Update Inventory"):
        update_inventory(product, new_stock)

elif options == "Log Damaged Stock":
    st.header("Log Damaged Stock")
    product = st.selectbox("Product:", list(inventory.keys()))
    damaged_quantity = st.number_input("Damaged Quantity (kg):", value=0)
    if st.button("Log Damaged Stock"):
        log_damage(product, damaged_quantity)

elif options == "Log Transport Delay":
    st.header("Log Transport Delay")
    product = st.selectbox("Product:", list(inventory.keys()))
    delay_days = st.number_input("Delay Duration (days):", value=0)
    if st.button("Log Transport Delay"):
        log_transport_delay(product, delay_days)

elif options == "View Inventory Status":
    st.header("View Inventory Status")
    view_inventory()
    plot_inventory_status()