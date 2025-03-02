Key functionalities of milestone 4:

Overview

The Sugar Supply Chain Management System is a real-time inventory management and risk prediction tool designed to monitor sugar stock levels, predict supply chain risks, and automate alerts. It is built using Streamlit, Machine Learning, and Slack integration to ensure efficient tracking and management of sugar inventory.

Features

1. Risk Factor Prediction

Uses a trained machine learning model (Random Forest Regressor) to predict the risk factor for inventory disruption.

Considers input factors such as:

Sentiment Score (from external sources like news sentiment analysis)

Transport Status

Lead Time (days)

Geopolitical Risk Level

Route Risk Level

2. Inventory Management

Maintains a database of sugar inventory with attributes:

Capacity: Maximum stock storage limit.

Current Stock: The amount of available sugar.

Monthly Purchase & Sales: Tracks stock flow.

Minimum Stock: The threshold for triggering restocking alerts.

Damaged Stock: Logs losses due to damage.

Transport Delay: Flags delays in delivery.

3. Automated Slack Alerts

Sends notifications via Slack when:

Stock falls below the minimum threshold.

Stock exceeds capacity.

High damage is logged.

Transport delays are recorded.

High supply chain risk is predicted.

4. Inventory Updates & Logging

Update Inventory: Allows users to manually adjust stock levels.

Log Damaged Stock: Deducts damaged stock from inventory and triggers necessary alerts.

Log Transport Delay: Records delays in sugar transportation and sends alerts.

5. Inventory Visualization

Displays bar charts of:

Current stock levels

Minimum stock threshold

Capacity

Helps users quickly assess stock status.

Installation

Prerequisites

Ensure you have Python 3.11 and the following libraries installed:

pip install streamlit pandas joblib scikit-learn requests matplotlib

Running the Application

Clone the repository or download the script.

Place the trained risk_factor_model.pkl, scaler.pkl, and label_encoders.pkl files in the project directory.

Start the Streamlit application:

streamlit run app.py

How to Use

Select an option from the sidebar:

Predict Risk Factor

Update Inventory

Log Damaged Stock

Log Transport Delay

View Inventory Status

Input required details (e.g., lead time, sentiment score, stock updates).

View predictions, alerts, and inventory reports.

Monitor Slack notifications for real-time updates.

Technologies Used

Streamlit: Web-based UI for interaction

Scikit-learn: Machine Learning model for risk prediction

Joblib: Model persistence and data transformation

Slack API: Automated alerts

Matplotlib: Data visualization

Pandas: Data manipulation

Future Enhancements

Expand inventory management to multiple products.

Integrate real-time sentiment analysis.

Add database storage (SQLite/PostgreSQL) for persistent tracking.

Improve UI/UX with additional visual insights.

License

This project is open-source and available for modification and enhancement.

