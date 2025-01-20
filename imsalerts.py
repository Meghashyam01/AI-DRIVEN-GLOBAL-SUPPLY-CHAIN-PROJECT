import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def create_inventory_dataset(file_path, num_rows=1000):
    """
    Generate a synthetic inventory dataset and save it to a CSV file.
    """
    random.seed(42)
    data = {
        'Month': [f'Month-{i % 12 + 1}' for i in range(num_rows)],
        'Utilization': [round(random.uniform(0.1, 1.0), 2) for _ in range(num_rows)],
        'Risk Score': [round(random.uniform(1, 10), 2) for _ in range(num_rows)],
        'Sentiment Score': [round(random.uniform(0, 10), 2) for _ in range(num_rows)],
        'Action': [random.choice(['SELL', 'MONITOR', 'BUY']) for _ in range(num_rows)]
    }
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"Dataset created and saved as {file_path}")

def analyze_inventory(file_path):
    """
    Analyze the inventory data and generate alerts based on thresholds.
    """
    data = pd.read_csv(file_path)

    alerts = []
    for _, row in data.iterrows():
        if row['Utilization'] > 0.8:
            alerts.append((row['Month'], "SELL", f"High utilization ({row['Utilization']:.2f}), consider reducing inventory."))
        elif row['Utilization'] < 0.4:
            alerts.append((row['Month'], "BUY", f"Low utilization ({row['Utilization']:.2f}), consider restocking."))
        else:
            alerts.append((row['Month'], "MONITOR", "Utilization is within normal range."))

    print("Generated Alerts:")
    for alert in alerts[:10]:  # Display first 10 alerts for brevity
        print(f"Month: {alert[0]}, Action: {alert[1]}, Reason: {alert[2]}")

    return data

def train_and_evaluate_model(file_path):
    """
    Train a Random Forest Classifier on the inventory dataset and evaluate it.
    """
    # Load and preprocess the dataset
    data = pd.read_csv(file_path)
    data['Action'] = data['Action'].map({'SELL': 0, 'MONITOR': 1, 'BUY': 2})

    X = data[['Utilization', 'Risk Score', 'Sentiment Score']]
    y = data['Action']

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the Random Forest model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return model

def predict_action(model, utilization, risk_score, sentiment_score):
    """
    Predict the action for new input data using the trained model.
    """
    new_input = pd.DataFrame({
        'Utilization': [utilization],
        'Risk Score': [risk_score],
        'Sentiment Score': [sentiment_score]
    })
    action_map = {0: 'SELL', 1: 'MONITOR', 2: 'BUY'}
    prediction = model.predict(new_input)
    print("\nPredicted Action:", action_map[prediction[0]])

# Step 1: Create the inventory dataset
file_path = "supply_chain_alerts_large.csv"
create_inventory_dataset(file_path, num_rows=1000)

# Step 2: Analyze inventory and generate alerts
data = analyze_inventory(file_path)

# Step 3: Train and evaluate the machine learning model
trained_model = train_and_evaluate_model(file_path)

# Step 4: Predict action for new data
predict_action(trained_model, utilization=0.85, risk_score=9.5, sentiment_score=5.0)
