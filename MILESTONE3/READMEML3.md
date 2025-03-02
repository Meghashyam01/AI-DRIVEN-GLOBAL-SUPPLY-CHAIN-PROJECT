Key functionalities of milestone 3:

Overview

The Sugar Supply Chain Management System is designed to enhance inventory tracking and risk management by integrating machine learning-based risk prediction with an inventory management system (IMS). This system helps in mitigating supply chain disruptions, optimizing stock levels, and ensuring smooth operations by predicting potential risks.

Key Features

Inventory Management System (IMS)

The Inventory Management System (IMS) in this project plays a crucial role in monitoring and managing the sugar supply chain. It includes:

Real-time Inventory Tracking:

Tracks current stock levels, monthly purchases, sales, and damaged goods.

Ensures inventory is within a healthy range, preventing overstocking or shortages.

Automated Stock Updates:

Updates inventory levels based on sales and incoming stock.

Adjusts stock for damaged goods and transport delays.

Inventory Alerts & Notifications:

Triggers alerts if stock falls below the minimum threshold.

Warns if stock exceeds capacity to prevent waste.

Generates warnings for transport delays affecting replenishment.

Interactive Data Visualization:

Provides a graphical representation of inventory status using bar charts.

Helps in decision-making by showcasing stock trends.

Risk Prediction Model

Predicts Supply Chain Risks:

Uses a Random Forest Classifier to analyze factors like sentiment score, transport status, lead time, geopolitical risk, and route risk level.

Helps businesses prepare for potential disruptions.

Machine Learning Model:

The model is trained on historical data, learning patterns to predict risk levels accurately.

Standardized preprocessing using Label Encoding and Feature Scaling.

Logging & Event Tracking

Log Damaged Stock:

Records damaged stock and updates the inventory accordingly.

Log Transport Delays:

Tracks supply chain delays and warns about potential disruptions.

Sales Tracking:

Keeps record of monthly sales and adjusts stock dynamically.

Ensures data consistency across sessions.

Interactive Web App

Built using Streamlit to provide a user-friendly interface.

Real-time interactive widgets for:

Risk Prediction based on input features.

Inventory Updates, including stock changes and sales.

Visualization of stock trends.

Installation & Requirements

Prerequisites

Python 3.11+

Libraries Required:

pip install pandas sklearn joblib streamlit matplotlib

Run the Streamlit App

streamlit run app.py

Interact with the Web Interface to predict risks, update inventory, and visualize stock trends.

Future Enhancements

More granular risk categorization using deep learning.

Automated inventory restocking suggestions.

Multi-product support with expanded inventory capabilities.

This Sugar Supply Chain Management System bridges the gap between inventory tracking and predictive analytics, ensuring smooth supply chain operations through AI-driven insights and real-time inventory management. 🚀