Risk Factorization:

Overview

This project trains a Random Forest Classifier to predict the risk factor of a supply chain based on various factors such as sentiment score, transport status, lead time, geopolitical risk, and route risk level. The trained model is saved for future use and can make real-time predictions based on user input.

Features

Data Preprocessing: Encodes categorical variables and standardizes numerical features.

Model Training: Uses a Random Forest Classifier to predict the risk factor.

Model Persistence: Saves the trained model, scaler, and label encoders for reuse.

Real-time Prediction: Accepts user input to predict risk factors dynamically.

Technologies Used

Python: Core programming language.

pandas: Data manipulation and preprocessing.

scikit-learn: Machine learning library for training and standardization.

joblib: For saving and loading the trained model.

Dataset

The dataset used for training is added_transportdelays_with_risk.csv, which contains:

Sentiment Score: Numeric value representing sentiment analysis of supply chain news.

Transport Status: Categorical variable indicating the transport condition.

Lead Time (days): Numeric value showing lead time.

Geopolitical Risk: Categorical variable (Low, Medium, High).

Route Risk Level: Numeric value representing risk associated with the route.

Risk Factor: The target variable to predict.

Code Workflow

1. Data Preprocessing

Categorical features (Transport Status, Geopolitical Risk) are encoded using LabelEncoder.

Numerical features are standardized using StandardScaler.

2. Model Training

A Random Forest Classifier is trained on the processed dataset.

The model, along with the scaler and label encoders, is saved using joblib.

3. Model Loading & Prediction

The saved model and preprocessing tools are loaded for inference.

User input is processed, encoded, and standardized before making a prediction.

The model predicts the Risk Factor based on the given inputs.

Output Files

risk_factor_model.pkl - Trained model.

scaler.pkl - StandardScaler object for feature scaling.

label_encoders.pkl - Dictionary containing label encoders for categorical features.

Usage Instructions

Install Dependencies:

pip install pandas scikit-learn joblib

Ensure the dataset added_transportdelays_with_risk.csv is available.

Run the script to train the model and make predictions.

Enter the required input values at runtime to get the predicted risk factor.

Future Enhancements

Improve model performance with hyperparameter tuning.

Add more features for better prediction accuracy.

Implement a web-based interface for easier access.

This project provides an efficient way to predict risk factors in supply chains using machine learning techniques.